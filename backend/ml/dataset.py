"""
Stanford Dogs Dataset PyTorch 加载器
支持 train/val/test 划分、XML 标注解析、可选 bounding box crop
"""

import os
import logging
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional, Tuple, List, Dict
from collections import defaultdict

import numpy as np
import torch
from PIL import Image
from torch.utils.data import Dataset, random_split

from .config import IMAGE_DIR, ANNOTATION_DIR, TRAIN_RATIO, VAL_RATIO, TEST_RATIO, NUM_WORKERS
from .breed_mapping import SYNSET_TO_CLASS, NUM_CLASSES

logger = logging.getLogger(__name__)


def parse_xml_annotation(xml_path: str) -> List[Dict]:
    """解析 PASCAL VOC XML 标注，返回所有目标边界框"""
    objects = []
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        for obj in root.findall("object"):
            name = obj.find("name").text
            bndbox = obj.find("bndbox")
            objects.append({
                "name": name,
                "xmin": int(bndbox.find("xmin").text),
                "ymin": int(bndbox.find("ymin").text),
                "xmax": int(bndbox.find("xmax").text),
                "ymax": int(bndbox.find("ymax").text),
            })
    except Exception as e:
        logger.debug(f"解析 XML 失败 {xml_path}: {e}")
    return objects


def crop_to_bbox(image: Image.Image, bbox: Dict, padding: float = 0.1) -> Image.Image:
    """
    按边界框裁剪，带 10% padding
    """
    w, h = image.size
    xmin = max(0, int(bbox["xmin"] - padding * w))
    ymin = max(0, int(bbox["ymin"] - padding * h))
    xmax = min(w, int(bbox["xmax"] + padding * w))
    ymax = min(h, int(bbox["ymax"] + padding * h))
    return image.crop((xmin, ymin, xmax, ymax))


class StanfordDogsDataset(Dataset):
    """
    Stanford Dogs Dataset PyTorch Dataset.
    
    参数:
        root_dir: 图片根目录 (e.g., images/Images/)
        annotation_dir: 标注根目录 (e.g., annotations/Annotation/)
        transform: torchvision transforms
        use_bbox_crop: 是否使用 XML 标注裁剪到边界框
        mode: "train" | "val" | "test" | "all"
        split_seed: 随机种子，保证可复现
    """

    def __init__(
        self,
        root_dir: str = None,
        annotation_dir: str = None,
        transform=None,
        use_bbox_crop: bool = False,
        mode: str = "train",
        split_seed: int = 42,
    ):
        self.root_dir = Path(root_dir) if root_dir else IMAGE_DIR
        self.annotation_dir = Path(annotation_dir) if annotation_dir else ANNOTATION_DIR
        self.transform = transform
        self.use_bbox_crop = use_bbox_crop
        self.mode = mode
        self.split_seed = split_seed

        # 收集所有图片路径和标签
        self.samples: List[Tuple[str, int]] = []
        self._load_samples()

        # 划分数据集
        if mode in ("train", "val", "test"):
            self._split_dataset()

        logger.info(f"StanfordDogsDataset [{mode}]: {len(self.samples)} 样本")

    def _load_samples(self):
        """扫描目录收集所有 (image_path, class_idx) 对"""
        all_samples = []
        for breed_dir in sorted(self.root_dir.iterdir()):
            if not breed_dir.is_dir():
                continue
            synset_id = breed_dir.name.split("-")[0]  # "n02085620" from "n02085620-Chihuahua"
            if synset_id not in SYNSET_TO_CLASS:
                logger.warning(f"未知 synset_id: {synset_id} (目录: {breed_dir.name})，跳过")
                continue
            class_idx = SYNSET_TO_CLASS[synset_id]
            for img_file in breed_dir.glob("*.jpg"):
                all_samples.append((str(img_file), class_idx))

        if not all_samples:
            raise RuntimeError(
                f"在 {self.root_dir} 中未找到任何图片。"
                f"请确保数据集已解压到正确位置。"
            )
        
        self._all_samples = all_samples
        assert len(set(s[1] for s in all_samples)) == NUM_CLASSES, \
            f"期望 {NUM_CLASSES} 个类别，实际找到 {len(set(s[1] for s in all_samples))}"

    def _split_dataset(self):
        """按预设比例划分 train/val/test"""
        n_total = len(self._all_samples)
        n_train = int(n_total * TRAIN_RATIO)
        n_val = int(n_total * VAL_RATIO)
        n_test = n_total - n_train - n_val

        generator = torch_generator(self.split_seed)
        splits = [n_train, n_val, n_test]

        subsets = random_split(self._all_samples, splits, generator=generator)

        if self.mode == "train":
            self.samples = subsets[0]
        elif self.mode == "val":
            self.samples = subsets[1]
        elif self.mode == "test":
            self.samples = subsets[2]

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        img_path, class_idx = self.samples[idx]
        image = Image.open(img_path).convert("RGB")

        # 可选: 使用 bounding box 裁剪
        if self.use_bbox_crop:
            xml_file = self.annotation_dir / Path(img_path).parent.name / (Path(img_path).stem)
            if xml_file.exists():
                objects = parse_xml_annotation(str(xml_file))
                if objects:
                    image = crop_to_bbox(image, objects[0])

        if self.transform:
            image = self.transform(image)

        return image, class_idx

    def get_class_distribution(self) -> Dict[int, int]:
        """获取各类别样本数分布"""
        dist = defaultdict(int)
        for _, cls in self.samples:
            dist[cls] += 1
        return dict(dist)

    @property
    def num_classes(self) -> int:
        return NUM_CLASSES


def torch_generator(seed: int = 42):
    """创建可复现的 PyTorch 随机数生成器"""
    return torch.Generator().manual_seed(seed)


def create_dataloaders(
    batch_size: int = 32,
    use_bbox_crop: bool = False,
    train_transform=None,
    val_transform=None,
    num_workers: int = NUM_WORKERS,
    split_seed: int = 42,
):
    """创建 train/val/test DataLoader"""
    from torch.utils.data import DataLoader

    if train_transform is None:
        from .preprocess import get_train_transforms
        train_transform = get_train_transforms()
    if val_transform is None:
        from .preprocess import get_val_transforms
        val_transform = get_val_transforms()

    ds_train = StanfordDogsDataset(transform=train_transform, use_bbox_crop=use_bbox_crop, mode="train", split_seed=split_seed)
    ds_val = StanfordDogsDataset(transform=val_transform, use_bbox_crop=use_bbox_crop, mode="val", split_seed=split_seed)
    ds_test = StanfordDogsDataset(transform=val_transform, use_bbox_crop=use_bbox_crop, mode="test", split_seed=split_seed)

    loader_train = DataLoader(ds_train, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    loader_val = DataLoader(ds_val, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    loader_test = DataLoader(ds_test, batch_size=batch_size, shuffle=False, num_workers=num_workers)

    return loader_train, loader_val, loader_test
