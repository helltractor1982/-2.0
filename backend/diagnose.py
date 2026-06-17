import sys
sys.path.insert(0, r'E:\dog_doctor\dog-doctor\backend')

import torch
from PIL import Image
import numpy as np

# 1. 加载模型 checkpoint
ckpt = torch.load(r'E:\dog_doctor\dog-doctor\backend\ml\models\best_model.pth', map_location='cpu')
print("=== Checkpoint 信息 ===")
print("Keys:", list(ckpt.keys()))
print("model_type:", ckpt.get("model_type"))
print("num_classes:", ckpt.get("num_classes"))
print("class_names 数量:", len(ckpt.get("class_names", [])))
print()

# 2. 检查 class_names 格式
class_names = ckpt["class_names"]
print("=== class_names 样本 ===")
for i in range(5):
    print(f"  idx {i}: '{class_names[i]}'")
print()

# 3. 加载 inference engine 并做真实推理测试
from ml.inference import InferenceEngine

engine = InferenceEngine()
success = engine.load_model()
print("=== InferenceEngine 加载结果 ===")
print("加载成功:", success)
print("_kaggle_class_names 数量:", len(engine._kaggle_class_names) if engine._kaggle_class_names else 'None')
print("_kaggle_to_local 映射数:", len(engine._kaggle_to_local) if engine._kaggle_to_local else 'None')
print()

# 4. 检查映射是否正确
print("=== 映射正确性检查 (前10个) ===")
for i in range(10):
    kname = engine._kaggle_class_names[i]
    breed = engine._kaggle_to_local.get(i)
    if breed:
        print(f"  idx {i}: kaggle='{kname}' -> breed_id={breed['breed_id']}, name_zh={breed['name_zh']}, name_en={breed['name_en']}")
    else:
        print(f"  idx {i}: kaggle='{kname}' -> NOT MAPPED")
print()

# 5. 用一张真实图片测试推理
print("=== 推理测试 ===")
# 创建一个伪图片（随机噪声）来测试推理输出
dummy_img = Image.fromarray(np.random.randint(0, 255, (224, 224, 3)).astype('uint8'))
result = engine.predict(dummy_img, top_k=5)
print("推理结果:")
if result.get("success"):
    for r in result["results"]:
        print(f"  class_idx={r['class_idx']}, breed_id={r['breed_id']}, name_zh={r['name_zh']}, name_en={r['name_en']}, conf={r['confidence']:.4f}")
else:
    print("  推理失败:", result.get("error"))
print()

# 6. 检查 breeds_data.py 的 name_en 格式
print("=== breeds_data.py name_en 格式检查 ===")
from breeds_data import BREEDS_DATA
print("breeds_data 品种数量:", len(BREEDS_DATA))
print("前5个品种的 name_en:")
for b in BREEDS_DATA[:5]:
    print(f"  breed_id={b['breed_id']}, name_en='{b['name_en']}', name_zh='{b['name_zh']}'")
print()

# 7. 检查 find_data_breed_id 是否能正确匹配
print("=== find_data_breed_id 匹配测试 ===")
from ml.breed_mapping import find_data_breed_id, normalize_breed_name
test_names = ["Chihuahua", "Japanese_spaniel", "Maltese_dog", "golden_retriever", "Labrador_retriever"]
for name in test_names:
    normalized = normalize_breed_name(name)
    found_id = find_data_breed_id(name)
    print(f"  '{name}' -> normalized='{normalized}' -> breed_id={found_id}")
print()

# 8. 检查 _enrich_results 的匹配
print("=== _enrich_results 匹配测试 ===")
from ml.breed_mapping import find_data_breed_by_name_en
for name in test_names:
    breed = find_data_breed_by_name_en(name)
    if breed:
        print(f"  '{name}' -> found: breed_id={breed['breed_id']}, name_zh={breed['name_zh']}")
    else:
        print(f"  '{name}' -> NOT FOUND")
