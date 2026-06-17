"""
推理模块: 模型加载、预处理、前向推理、结果解析
集成 breeds_data.py 提供品种特征与疾病信息
"""

import time
import logging
from typing import List, Dict, Optional
from pathlib import Path

import torch
import torch.nn as nn
import numpy as np
from PIL import Image

from .config import (
    MODEL_PATH, TOP_K, CONFIDENCE_THRESHOLD, DEVICE,
    USE_HALF_PRECISION,
)
from .breed_mapping import CLASS_TO_BREED_ID, NUM_CLASSES
from .preprocess import decode_base64_image, preprocess_for_inference

logger = logging.getLogger(__name__)


class InferenceEngine:
    """
    犬种识别推理引擎
    
    用法:
        engine = InferenceEngine()
        engine.load_model()
        results = engine.predict(image_or_base64)
        # results = [{"breed_id": "057", "name_zh": "金毛寻回犬", "confidence": 0.92, ...}, ...]
    """

    def __init__(self, model_path: str = None, device: str = None):
        self.model_path = Path(model_path) if model_path else MODEL_PATH
        self.device = torch.device(device or (DEVICE if torch.cuda.is_available() else "cpu"))
        self.model: Optional[nn.Module] = None
        self._loaded = False
        self._kaggle_class_names = None  # Kaggle训练的类别名列表
        self._kaggle_to_local = None     # Kaggle class_idx -> 本地 breed_id 映射
        logger.info(f"InferenceEngine 初始化，设备: {self.device}")

    def load_model(self, force_reload: bool = False) -> bool:
        """加载训练好的模型"""
        if self._loaded and not force_reload:
            return True

        if not self.model_path.exists():
            logger.error(f"模型文件不存在: {self.model_path}")
            logger.info("请先运行训练: python -m backend.ml.train --mode full")
            return False

        try:
            from .model import build_model, KaggleResNetClassifier, ResNet50CBAMClassifier, EfficientNetCBAMClassifier
            checkpoint = torch.load(self.model_path, map_location=self.device, weights_only=False)

            # 支持三种模型格式:
            # 1. 新版训练格式: {"model_state": ..., "class_names": [synset_ids], "num_classes": 120}
            #    state_dict key 无前缀, 有 cbam / fc / features+classifier 等自定义模块
            # 2. 旧版 Kaggle 格式: {"model_state": ..., "class_names": ["n02xxx-Name"], ...}
            # 3. 直接 state_dict 格式 (本地训练, DogBreedClassifier)
            if isinstance(checkpoint, dict) and "model_state" in checkpoint:
                state_dict = checkpoint["model_state"]
                num_classes = checkpoint.get("num_classes", NUM_CLASSES)
                kaggle_class_names = checkpoint.get("class_names", [])
            else:
                state_dict = checkpoint
                num_classes = NUM_CLASSES
                kaggle_class_names = []

            # 判断模型格式:
            # - class_names 非空 -> 来自训练脚本（含新版/旧版 Kaggle）
            # - 否则 -> 本地训练
            is_trained_checkpoint = (isinstance(checkpoint, dict) and
                                     checkpoint.get("class_names") and
                                     len(checkpoint["class_names"]) > 0)

            if is_trained_checkpoint:
                # 通过 state_dict key 特征判断具体架构
                first_key = next(iter(state_dict.keys()))
                has_cbam = any("cbam" in k for k in state_dict.keys())
                has_features = any(k.startswith("features.") for k in state_dict.keys())

                if has_cbam and has_features:
                    # EfficientNet + CBAM 架构（新版训练）
                    self.model = EfficientNetCBAMClassifier(num_classes=num_classes)
                    self.model.load_state_dict(state_dict)
                    logger.info("加载新版训练模型 (EfficientNetB0 + CBAM 格式)")
                elif has_cbam and not has_features:
                    # ResNet50 + CBAM 架构（新版训练）
                    self.model = ResNet50CBAMClassifier(num_classes=num_classes)
                    self.model.load_state_dict(state_dict)
                    logger.info("加载新版训练模型 (ResNet50 + CBAM 格式)")
                elif first_key.startswith("backbone.") or first_key.startswith("classifier."):
                    # DogBreedClassifier 格式（旧版 kaggle_train.py v2 训练）
                    self.model = build_model(num_classes=num_classes, pretrained=False)
                    self.model.load_state_dict(state_dict)
                    logger.info("加载 Kaggle 训练模型 (DogBreedClassifier 格式)")
                else:
                    # 原始 ResNet 格式（旧版 kaggle 训练，单层 fc）
                    self.model = KaggleResNetClassifier(num_classes=num_classes)
                    self.model.load_kaggle_state_dict(state_dict)
                    logger.info("加载 Kaggle 训练模型 (原始 ResNet 格式)")

                # 构建 class_names -> 本地 breed_id 映射
                self._kaggle_class_names = kaggle_class_names
                if self._kaggle_class_names:
                    self._kaggle_to_local = self._build_kaggle_mapping(self._kaggle_class_names)
                    logger.info(f"类别映射已构建: {len(self._kaggle_to_local)}/{len(self._kaggle_class_names)} 个品种")
                    # 打印未映射的类别
                    unmapped = [i for i in range(len(self._kaggle_class_names)) if i not in self._kaggle_to_local]
                    if unmapped:
                        logger.warning(f"未映射的类别 ({len(unmapped)} 个):")
                        for i in unmapped[:5]:
                            logger.warning(f"  idx {i}: {self._kaggle_class_names[i]}")
            else:
                # 本地训练模型
                if not isinstance(checkpoint, dict) or "model_state" not in checkpoint:
                    state_dict = checkpoint
                    num_classes = NUM_CLASSES
                self.model = build_model(num_classes=num_classes, pretrained=False)
                self.model.load_state_dict(state_dict)
                self._kaggle_class_names = None
                self._kaggle_to_local = None
                logger.info("加载本地训练模型 (DogBreedClassifier 格式)")

            self.model.to(self.device)
            self.model.eval()

            if USE_HALF_PRECISION and self.device.type == "cuda":
                self.model.half()

            self._loaded = True
            logger.info(f"模型加载成功: {self.model_path}")
            return True
        except Exception as e:
            logger.exception(f"模型加载失败: {e}")
            return False

    def _build_kaggle_mapping(self, kaggle_names: list) -> dict:
        """
        构建 Kaggle class_idx -> 本地 breed 信息的映射。

        支持两种 class_name 格式:
        1. 纯 synset_id 格式: "n02085620"  (新版训练脚本)
        2. synset_id-英文名格式: "n02085620-Chihuahua" (旧版 Kaggle 格式)

        匹配策略（按优先级）:
        1. synset_id 精确匹配（最可靠，优先使用）
        2. 英文名精确匹配（忽略大小写和下划线/空格）
        3. 英文名模糊匹配（去除所有分隔符）
        4. 子串匹配（处理名称变体）

        重要: synset_id 优先于英文名，因为不同数据集中同名品种
        可能对应不同的 synset_id（如 Japanese_spaniel 对应
        n02085360 和 n02085782 两个不同的 synset）。
        """
        from .breed_mapping import SYNSET_TO_BREED, NAME_EN_TO_BREED, BREED_MAP
        mapping = {}

        for idx, name in enumerate(kaggle_names):
            breed = None
            name = name.strip()

            # 判断格式: 纯 synset_id（如 n02085620）还是 synset_id-英文名
            parts = name.split('-', 1)

            if len(parts) == 1:
                # 纯 synset_id 格式（新版训练脚本）
                synset_id = parts[0]
                breed = SYNSET_TO_BREED.get(synset_id)
            else:
                synset_id = parts[0]
                english_name = parts[1]
                # NAME_EN_TO_BREED 的 key 使用下划线格式（如 toy_terrier）
                clean_name_underscore = english_name.strip().lower()
                clean_name_spaces = english_name.replace('_', ' ').strip().lower()

                # 策略1: synset_id 精确匹配（最高优先级，最可靠）
                breed = SYNSET_TO_BREED.get(synset_id)

                # 策略2: 英文名精确匹配（synset_id 不匹配时使用）
                if breed is None:
                    breed = NAME_EN_TO_BREED.get(clean_name_underscore)
                    if breed is None:
                        breed = NAME_EN_TO_BREED.get(clean_name_spaces)

                # 策略3: 模糊匹配（去除所有分隔符比较）
                if breed is None:
                    clean_no_sep = clean_name_underscore.replace('_', '').replace('-', '')
                    for b in BREED_MAP:
                        local_clean = b["name_en"].lower().replace('_', '').replace(' ', '').replace('-', '')
                        if local_clean == clean_no_sep:
                            breed = b
                            break

                # 策略4: 子串匹配（处理名称变体如 Standard_Poodle vs standard_poodle）
                if breed is None:
                    for b in BREED_MAP:
                        local_lower = b["name_en"].lower().replace('_', ' ')
                        if clean_name_spaces in local_lower or local_lower in clean_name_spaces:
                            if len(clean_name_spaces) >= 5 and len(local_lower) >= 5:
                                breed = b
                                break

            if breed:
                mapping[idx] = breed
            else:
                logger.warning(f"Kaggle 类别 {idx} '{name}' 无法匹配到本地品种映射")

        return mapping

    @property
    def is_loaded(self) -> bool:
        return self._loaded

    def predict(
        self,
        image_input,
        top_k: int = TOP_K,
        remove_bg: bool = False,
    ) -> Dict:
        """
        识别犬种
        
        参数:
            image_input: PIL.Image 或 base64 字符串
            top_k: 返回 Top-K 结果数
            remove_bg: 是否去除背景
        
        返回:
            {
                "success": True/False,
                "results": [{"breed_id": str, "name_zh": str, "name_en": str,
                             "class_idx": int, "confidence": float}, ...],
                "inference_time_ms": float,
                "error": str (if failed)
            }
        """
        if not self._loaded:
            if not self.load_model():
                return {"success": False, "results": [], "error": "模型未加载"}

        t_start = time.time()

        try:
            # 1. 输入处理
            if isinstance(image_input, str):
                image = decode_base64_image(image_input)
            elif isinstance(image_input, Image.Image):
                image = image_input
            else:
                return {"success": False, "results": [], "error": f"不支持的输入类型: {type(image_input)}"}

            # 2. 预处理
            tensor = preprocess_for_inference(image, remove_bg=remove_bg).to(self.device)
            if USE_HALF_PRECISION and self.device.type == "cuda":
                tensor = tensor.half()

            # 3. 推理
            with torch.no_grad():
                outputs = self.model(tensor)
                probabilities = torch.softmax(outputs, dim=1)

            # 4. 后处理: Top-K
            probs, indices = torch.topk(probabilities, k=min(top_k, NUM_CLASSES), dim=1)
            probs = probs.cpu().numpy()[0]
            indices = indices.cpu().numpy()[0]

            # 5. 构建结果
            results = []
            for cls_idx, conf in zip(indices, probs):
                conf = float(conf)
                if conf < CONFIDENCE_THRESHOLD:
                    break

                cls_idx = int(cls_idx)

                # 如果是 Kaggle 训练模型，使用 Kaggle 映射
                if self._kaggle_to_local is not None:
                    breed = self._kaggle_to_local.get(cls_idx)
                    if breed:
                        breed_id = breed["breed_id"]
                        name_zh = breed["name_zh"]
                        name_en = breed["name_en"]
                    else:
                        continue
                else:
                    breed_id = CLASS_TO_BREED_ID.get(cls_idx)
                    if not breed_id:
                        continue
                    from .breed_mapping import CLASS_TO_BREED
                    breed_info = CLASS_TO_BREED.get(cls_idx, {})
                    name_zh = breed_info.get("name_zh", "")
                    name_en = breed_info.get("name_en", "")

                results.append({
                    "breed_id": breed_id,
                    "name_zh": name_zh,
                    "name_en": name_en,
                    "class_idx": cls_idx,
                    "confidence": round(conf, 4),
                })

            inference_time_ms = (time.time() - t_start) * 1000

            # 6. 补充品种详细信息（从 breeds_data.py）
            results = self._enrich_results(results)

            return {
                "success": True,
                "results": results,
                "top_result": results[0] if results else None,
                "inference_time_ms": round(inference_time_ms, 1),
            }

        except Exception as e:
            logger.exception("推理失败")
            return {"success": False, "results": [], "error": str(e)}

    def _enrich_results(self, results: List[Dict]) -> List[Dict]:
        """
        用 breeds_data.py 的完整品种数据丰富识别结果
        
        重要: 通过 name_en 匹配 breeds_data, 因为 breed_mapping 和 
        breeds_data 使用不同的 breed_id 编号体系。
        只补充详细信息, 不覆盖 name_zh/name_en/breed_id。
        """
        try:
            from .breed_mapping import find_data_breed_by_name_en

            for r in results:
                breed = find_data_breed_by_name_en(r.get("name_en", ""))
                if breed:
                    r.update({
                        "origin": breed.get("origin", ""),
                        "size": breed.get("size", ""),
                        "weight_range": breed.get("weight_range", ""),
                        "height_range": breed.get("height_range", ""),
                        "lifespan": breed.get("lifespan", ""),
                        "personality": breed.get("personality", []),
                        "coat_color": breed.get("coat_color", []),
                        "coat_length": breed.get("coat_length", ""),
                        "shedding": breed.get("shedding", ""),
                        "exercise_need": breed.get("exercise_need", ""),
                        "feeding_tips": breed.get("feeding_tips", ""),
                        "forbidden_foods": breed.get("forbidden_foods", []),
                        "common_diseases": breed.get("common_diseases", []),
                        "vaccine_schedule": breed.get("vaccine_schedule", ""),
                        "grooming": breed.get("grooming", ""),
                        "tags": breed.get("tags", []),
                        "description": breed.get("description", ""),
                    })
        except ImportError:
            logger.warning("无法导入 breeds_data，结果将不包含品种详细信息")
        except Exception as e:
            logger.warning(f"丰富品种信息失败: {e}")

        return results

    def predict_batch(
        self,
        images: List,
        top_k: int = TOP_K,
    ) -> List[Dict]:
        """批量识别"""
        return [self.predict(img, top_k=top_k) for img in images]

    def get_model_info(self) -> Dict:
        """获取模型信息"""
        info = {
            "model_type": "ResNet50",
            "num_classes": NUM_CLASSES,
            "device": str(self.device),
            "model_path": str(self.model_path),
            "is_loaded": self._loaded,
            "top_k": TOP_K,
            "confidence_threshold": CONFIDENCE_THRESHOLD,
        }
        if self.model_path.exists():
            import os
            info["model_size_mb"] = round(os.path.getsize(self.model_path) / (1024 * 1024), 2)
        return info


# 全局单例
_engine: Optional[InferenceEngine] = None


def get_engine(force_reload: bool = False) -> InferenceEngine:
    """获取全局推理引擎单例"""
    global _engine
    if _engine is None or force_reload:
        _engine = InferenceEngine()
        _engine.load_model()
    return _engine


# ====== FastAPI 集成接口 (main.py 调用) ======

def init_inference_engine(
    model_path: str,
    class_names: Optional[List[str]] = None,
    id_to_breedid: Optional[Dict[str, str]] = None,
) -> bool:
    """
    main.py 启动时调用的初始化函数
    加载模型并设置为全局推理引擎

    参数:
        model_path: 训练好的模型文件路径
        class_names: 类别中文名列表 (按 class_idx 顺序, 当前从 breed_mapping 自动获取)
        id_to_breedid: class_idx→breed_id 映射 (当前从 breed_mapping 自动获取)
    返回:
        是否加载成功
    """
    global _engine
    try:
        _engine = InferenceEngine(model_path=model_path)
        success = _engine.load_model()
        if success:
            logger.info(f"推理引擎初始化成功: {model_path}")
        else:
            logger.warning(f"推理引擎初始化失败: 模型文件不存在或损坏")
        return success
    except Exception as e:
        logger.error(f"推理引擎初始化异常: {e}")
        return False


def identify_dog_breed(image_base64: str, top_k: int = 3) -> Dict:
    """
    单张图片品种识别 (main.py /api/identify 调用)

    参数:
        image_base64: base64 编码的图片
        top_k: 返回 Top-K 结果
    返回:
        {"results": [...], "inference_time_ms": float}
    """
    global _engine
    if _engine is None:
        # 尝试默认路径加载
        _engine = InferenceEngine()
        if not _engine.load_model():
            return {"results": [], "inference_time_ms": 0, "error": "模型未加载"}

    raw = _engine.predict(image_base64, top_k=top_k)

    if not raw.get("success"):
        return {"results": [], "inference_time_ms": 0, "error": raw.get("error", "推理失败")}

    # predict() 已经通过 _kaggle_to_local 或 CLASS_TO_BREED_ID
    # 正确填充了 breed_id / name_zh / name_en，
    # _enrich_results() 也已补充了详细信息。
    # 此处不再用 find_data_breed_id() 覆盖 breed_id，
    # 因为 breeds_data.py 的 name_en 格式与 breed_mapping.py 不一致，
    # 会导致错误映射。
    results = raw.get("results", [])
    return {
        "results": results,
        "inference_time_ms": raw.get("inference_time_ms", 0),
    }


def is_model_loaded() -> bool:
    """检查模型是否已加载 (main.py health check 调用)"""
    global _engine
    return _engine is not None and _engine.is_loaded
