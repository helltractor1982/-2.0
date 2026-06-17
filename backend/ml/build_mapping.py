"""
构建 breed_mapping ↔ breeds_data 对应关系
匹配现有 60 品种到 Stanford 120，生成缺失品种数据
"""

import re, json, sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent


def load_existing_breeds():
    """从 breeds_data.py 提取现有 60 品种"""
    with open(BACKEND_DIR / "breeds_data.py", "r", encoding="utf-8") as f:
        content = f.read()

    # 提取所有品种数据块
    breeds = []
    # 简单提取 name_en 和 breed_id
    ids = re.findall(r'"breed_id":\s*"(.+?)"', content)
    names_en = re.findall(r'"name_en":\s*"(.+?)"', content)
    for bid, name in zip(ids, names_en):
        breeds.append({"breed_id": bid, "name_en": name.lower()})
    return breeds


def load_stanford_breeds():
    """从 breed_mapping.py 加载 120 Stanford 品种"""
    sys.path.insert(0, str(BACKEND_DIR))
    from ml.breed_mapping import BREED_MAP
    return [{"synset_id": b["synset_id"], "class_idx": b["class_idx"],
             "name_en": b["name_en"].lower().replace("_", " "),
             "name_zh": b["name_zh"]} for b in BREED_MAP]


def normalize_name(name: str) -> str:
    """标准化品种名用于匹配"""
    name = name.lower().replace("_", " ").replace("-", " ")
    # 常见同义映射
    synonyms = {
        "poodle": "standard poodle",
        "english bulldog": "bulldog",
        "shiba inu": "shiba",
        "alaskan malamute": "malamute",
        "german shepherd": "german shepherd dog",
        "cocker spaniel": "cocker spaniel",
        "english springer spaniel": "english springer",
        "shetland sheepdog": "shetland sheepdog",
        "australian shepherd": "australian shepherd",
    }
    return synonyms.get(name, name)


def match_breeds(existing, stanford):
    """匹配现有品种到 Stanford 品种"""
    matched = {}
    unmatched_existing = []
    unmatched_stanford = list(range(len(stanford)))

    for i, eb in enumerate(existing):
        en = normalize_name(eb["name_en"])
        found = False
        for j, sb in enumerate(stanford):
            if j not in unmatched_stanford:
                continue
            sn = sb["name_en"]
            # 精确匹配或包含匹配
            if en == sn or en in sn or sn in en or en.replace(" ", "") == sn.replace(" ", ""):
                matched[i] = j  # existing_idx -> stanford_idx
                unmatched_stanford.remove(j)
                found = True
                break
        if not found:
            unmatched_existing.append(i)

    return matched, unmatched_existing, unmatched_stanford


def main():
    existing = load_existing_breeds()
    stanford = load_stanford_breeds()

    matched, unmatched_existing, unmatched_stanford = match_breeds(existing, stanford)

    print(f"现有品种: {len(existing)}")
    print(f"Stanford 品种: {len(stanford)}")
    print(f"匹配成功: {len(matched)}")
    print(f"现有未匹配: {len(unmatched_existing)}")
    print(f"Stanford 未匹配: {len(unmatched_stanford)}")

    if unmatched_existing:
        print("\n现有品种未匹配到 Stanford 数据集:")
        for i in unmatched_existing:
            print(f"  {existing[i]['breed_id']}: {existing[i]['name_en']}")

    # 构建映射表: class_idx -> breed_id (breeds_data 中的 ID)
    class_to_breed_id = {}
    breed_id_to_class = {}

    # 匹配到的: Stanford class_idx -> existing breed_id
    for exist_i, stanford_j in matched.items():
        class_idx = stanford[stanford_j]["class_idx"]
        breed_id = existing[exist_i]["breed_id"]
        class_to_breed_id[class_idx] = breed_id
        breed_id_to_class[breed_id] = class_idx

    # 未匹配的 Stanford 品种: 分配新 breed_id "061"-"120"
    next_id = 61
    new_breeds = []
    for j in unmatched_stanford:
        if next_id > 120:
            break
        breed_id = f"{next_id:03d}"
        class_idx = stanford[j]["class_idx"]
        class_to_breed_id[class_idx] = breed_id
        breed_id_to_class[breed_id] = class_idx
        new_breeds.append({
            "breed_id": breed_id,
            "synset_id": stanford[j]["synset_id"],
            "class_idx": class_idx,
            "name_zh": stanford[j]["name_zh"],
            "name_en": stanford[j]["name_en"].replace(" ", "_"),
        })
        next_id += 1

    # 保存映射
    mapping = {
        "class_to_breed_id": {str(k): v for k, v in class_to_breed_id.items()},
        "breed_id_to_class": breed_id_to_class,
        "num_matched": len(matched),
        "num_new": len(new_breeds),
    }

    mapping_path = BACKEND_DIR / "ml" / "data_mapping.json"
    with open(mapping_path, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    print(f"\n映射已保存到: {mapping_path}")

    # 输出需要新增的品种列表
    print(f"\n需要新增 {len(new_breeds)} 个品种到 breeds_data.py:")
    for nb in new_breeds:
        print(f"  {nb['breed_id']}: {nb['name_zh']} ({nb['name_en']}) -> synset={nb['synset_id']}, class={nb['class_idx']}")

    return new_breeds


if __name__ == "__main__":
    new_breeds = main()
