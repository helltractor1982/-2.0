"""
犬种识别验证脚本
================
用法: python test_inference.py <图片路径>
功能: 加载模型并对指定图片进行推理，显示详细的预测结果和映射信息。
"""
import sys
import json
from pathlib import Path

# 添加项目路径
PROJECT_ROOT = Path(r"E:\dog_doctor\dog-doctor")
sys.path.insert(0, str(PROJECT_ROOT))

import torch
from PIL import Image
from torchvision import transforms

from backend.ml.config import MEAN, STD, IMAGE_SIZE, RESIZE_SIZE
from backend.ml.breed_mapping import BREED_MAP, SYNSET_TO_BREED


def load_and_inspect_model(model_path):
    """加载模型并输出详细信息"""
    print(f"模型路径: {model_path}")
    print(f"文件大小: {Path(model_path).stat().st_size / 1024**2:.2f} MB")

    checkpoint = torch.load(model_path, map_location="cpu", weights_only=False)

    # 判断格式
    if isinstance(checkpoint, dict) and "model_state" in checkpoint:
        state_dict = checkpoint["model_state"]
        class_names = checkpoint.get("class_names", [])
        num_classes = checkpoint.get("num_classes", "?")
        print(f"格式: dict checkpoint (含 model_state)")
        print(f"num_classes: {num_classes}")
        print(f"class_names 数量: {len(class_names)}")
    else:
        state_dict = checkpoint
        class_names = []
        print(f"格式: 纯 state_dict")

    # 判断模型结构
    first_key = next(iter(state_dict.keys()))
    print(f"第一个 key: {first_key}")

    if first_key.startswith("backbone.") or first_key.startswith("classifier."):
        print("模型类型: DogBreedClassifier (自定义分类头)")
        from backend.ml.model import build_model
        model = build_model(num_classes=len(class_names) if class_names else 120, pretrained=False)
        model.load_state_dict(state_dict)
    else:
        print("模型类型: KaggleResNetClassifier (简单 fc 层)")
        from backend.ml.model import KaggleResNetClassifier
        nc = len(class_names) if class_names else 120
        model = KaggleResNetClassifier(num_classes=nc)
        model.load_kaggle_state_dict(state_dict)

    model.eval()

    # 映射分析
    if class_names:
        print("\n=== Class Names 映射分析 ===")
        synset_ok = 0
        en_ok = 0
        miss = 0
        for idx, name in enumerate(class_names):
            parts = name.split('-', 1)
            if len(parts) == 2:
                c_synset = parts[0]
                c_name = parts[1]
                if c_synset in SYNSET_TO_BREED:
                    synset_ok += 1
                else:
                    # 检查英文名
                    clean = c_name.strip().lower()
                    clean_sp = c_name.replace('_', ' ').strip().lower()
                    from backend.ml.breed_mapping import NAME_EN_TO_BREED
                    if NAME_EN_TO_BREED.get(clean) or NAME_EN_TO_BREED.get(clean_sp):
                        en_ok += 1
                    else:
                        miss += 1
                        print(f"  [MISS] idx {idx}: {name}")
            else:
                miss += 1
                print(f"  [MISS] idx {idx}: {name}")

        print(f"  synset 精确匹配: {synset_ok}")
        print(f"  英文名匹配: {en_ok}")
        print(f"  未匹配: {miss}")

        # 检查重复英文名
        en_names = []
        for name in class_names:
            parts = name.split('-', 1)
            if len(parts) == 2:
                en_names.append(parts[1].strip().lower().replace('_', ' '))

        dupes = [n for n in set(en_names) if en_names.count(n) > 1]
        if dupes:
            print(f"\n  [警告] 重复的英文名 ({len(dupes)} 个):")
            for d in dupes:
                print(f"    '{d}' 出现 {en_names.count(d)} 次")

    return model, class_names


def preprocess_image(image_path):
    """推理预处理"""
    img = Image.open(image_path).convert("RGB")
    transform = transforms.Compose([
        transforms.Resize(RESIZE_SIZE),
        transforms.CenterCrop(IMAGE_SIZE),
        transforms.ToTensor(),
        transforms.Normalize(mean=MEAN, std=STD),
    ])
    return transform(img).unsqueeze(0)


def predict_with_mapping(model, class_names, image_path, top_k=5):
    """推理并显示详细映射"""
    from backend.ml.breed_mapping import SYNSET_TO_BREED, NAME_EN_TO_BREED

    tensor = preprocess_image(image_path)

    with torch.no_grad():
        outputs = model(tensor)
        probs = torch.softmax(outputs, dim=1)
        top_probs, top_indices = torch.topk(probs, k=min(top_k, probs.size(1)))

    print(f"\n=== 推理结果 (图片: {Path(image_path).name}) ===")
    print(f"{'Rank':>4} | {'ClassIdx':>8} | {'Prob':>8} | {'Checkpoint Name':>35} | {'映射方式':>8} | {'匹配品种':>30} | {'匹配中文名':>15}")
    print("-" * 150)

    for rank, (prob, idx) in enumerate(zip(top_probs[0], top_indices[0])):
        idx = int(idx)
        prob = float(prob)

        if class_names and idx < len(class_names):
            ck_name = class_names[idx]
            parts = ck_name.split('-', 1)
            c_synset = parts[0] if len(parts) == 2 else "?"
            c_en_name = parts[1] if len(parts) == 2 else ck_name

            # 尝试匹配
            breed = SYNSET_TO_BREED.get(c_synset)
            method = "synset" if breed else None
            if not breed:
                clean = c_en_name.strip().lower()
                clean_sp = c_en_name.replace('_', ' ').strip().lower()
                breed = NAME_EN_TO_BREED.get(clean) or NAME_EN_TO_BREED.get(clean_sp)
                method = "en_name" if breed else "NONE"

            matched_name = breed["name_en"] if breed else "???"
            matched_zh = breed["name_zh"] if breed else "???"
        else:
            ck_name = "?"
            method = "NONE"
            matched_name = "?"
            matched_zh = "?"

        print(f"{rank+1:4d} | {idx:8d} | {prob:8.4f} | {ck_name:>35} | {method or 'NONE':>8} | {matched_name:>30} | {matched_zh:>15}")


def main():
    if len(sys.argv) < 2:
        print("用法: python test_inference.py <图片路径> [模型路径]")
        print("示例: python test_inference.py test.jpg")
        print("      python test_inference.py test.jpg E:\\dog_doctor\\dog-doctor\\backend\\ml\\models\\best_model.pth")
        sys.exit(1)

    image_path = sys.argv[1]
    model_path = sys.argv[2] if len(sys.argv) > 2 else PROJECT_ROOT / "backend" / "ml" / "models" / "best_model.pth"

    if not Path(image_path).exists():
        print(f"图片不存在: {image_path}")
        sys.exit(1)

    if not Path(model_path).exists():
        print(f"模型不存在: {model_path}")
        sys.exit(1)

    print("=" * 60)
    print("犬种识别验证脚本")
    print("=" * 60)

    model, class_names = load_and_inspect_model(str(model_path))
    predict_with_mapping(model, class_names, image_path, top_k=10)

    print("\n" + "=" * 60)
    print("验证完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
