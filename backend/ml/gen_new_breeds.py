"""
生成新增 60 个品种的数据条目，并更新推理映射
"""

import json, re
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent

# 加载匹配结果
with open(BACKEND_DIR / "ml" / "data_mapping.json", "r", encoding="utf-8") as f:
    mapping = json.load(f)

# 加载 Stanford 种信息
import sys
sys.path.insert(0, str(BACKEND_DIR))
from ml.breed_mapping import BREED_MAP, CLASS_TO_BREED

# class_to_breed_id 是 {"0": "061", "1": "062", ...}
class_to_breed_id = mapping["class_to_breed_id"]

# 已有 60 个，新增 60 个（breed_id "061"-"120"）
# 需要为每个新 breed_id 生成完整的品种数据

BREED_TEMPLATES = {
    "小型犬": {
        "size": "小型犬", "weight_range": "3-10 kg", "height_range": "20-35 cm",
        "lifespan": "12-16年", "exercise_need": "中等",
        "personality": ["活泼好动", "聪明机警", "友善亲人"],
        "coat_color": ["棕白", "黑白", "纯棕"],
        "coat_length": "短毛", "shedding": "中等",
        "feeding_tips": "建议每日喂食2-3次，选用小型犬专用粮，注意控制零食量",
        "forbidden_foods": ["巧克力", "葡萄", "洋葱", "大蒜", "木糖醇"],
        "recommended_food": "优质小型犬粮，可搭配适量鸡胸肉和蔬菜",
        "common_diseases": ["髌骨脱位", "牙齿问题", "气管塌陷", "眼疾"],
        "vaccine_schedule": "幼犬6-8周首免，之后每3-4周加强一次，成年后每年加强",
        "grooming": "每周梳毛2-3次，定期修剪指甲和清洁耳朵",
    },
    "中型犬": {
        "size": "中型犬", "weight_range": "15-30 kg", "height_range": "40-60 cm",
        "lifespan": "10-14年", "exercise_need": "中等",
        "personality": ["聪明忠诚", "友善温和", "精力充沛"],
        "coat_color": ["棕白", "黑白", "虎斑"],
        "coat_length": "中等", "shedding": "中等",
        "feeding_tips": "每日喂食2次，选用中型犬粮，根据运动量调整食量",
        "forbidden_foods": ["巧克力", "葡萄", "洋葱", "大蒜", "木糖醇"],
        "recommended_food": "中大型犬粮，搭配适量肉类和蔬菜",
        "common_diseases": ["髋关节发育不良", "皮肤病", "耳部感染", "过敏"],
        "vaccine_schedule": "幼犬6-8周首免，之后每3-4周加强一次，成年后每年加强",
        "grooming": "每周梳毛2-3次，定期洗澡和修剪指甲",
    },
    "大型犬": {
        "size": "大型犬", "weight_range": "25-45 kg", "height_range": "55-75 cm",
        "lifespan": "8-12年", "exercise_need": "高",
        "personality": ["勇敢忠诚", "沉稳冷静", "护卫性强"],
        "coat_color": ["黑色", "棕白", "灰色"],
        "coat_length": "中等", "shedding": "高",
        "feeding_tips": "每日喂食2次，选用大型犬粮，注意关节保健和钙质补充",
        "forbidden_foods": ["巧克力", "葡萄", "洋葱", "大蒜", "木糖醇", "高盐食物"],
        "recommended_food": "大型犬专用粮，可添加关节保健补充剂",
        "common_diseases": ["髋关节发育不良", "胃扭转", "心脏病", "关节炎"],
        "vaccine_schedule": "幼犬6-8周首免，之后每3-4周加强一次，成年后每年加强",
        "grooming": "每周梳毛2-3次，定期洗澡，关注指甲和牙齿健康",
    },
}

def guess_size(name_zh):
    """根据品种名推测体型"""
    small_keywords = ["迷你", "小型", "玩具", "吉娃娃", "蝴蝶", "博美", "约克夏", "巴哥",
                      "梗", "京巴", "贵宾", "西施", "马尔济斯", "腊肠"]
    large_keywords = ["大型", "巨型", "大丹", "圣伯纳", "纽芬兰", "大白熊", "藏獒",
                      "罗威纳", "猎狼", "猎鹿", "獒", "狼"]
    for kw in small_keywords:
        if kw in name_zh:
            return "small"
    for kw in large_keywords:
        if kw in name_zh:
            return "large"
    return "medium"

def generate_breed_entry(breed_id, class_idx):
    """为一个新品种生成完整的 breeds_data 条目"""
    breed_info = CLASS_TO_BREED[class_idx]
    name_zh = breed_info["name_zh"]
    name_en = breed_info["name_en"]

    size_cat = guess_size(name_zh)
    template = BREED_TEMPLATES[{"small": "小型犬", "medium": "中型犬", "large": "大型犬"}[size_cat]]

    description = f"{name_zh}是一种迷人的犬种，以其独特的性格和外貌受到许多爱犬人士的喜爱。{name_zh}适应家庭生活，是忠诚的伴侣犬。"

    entry = f'''    {{
        "breed_id": "{breed_id}",
        "name_zh": "{name_zh}",
        "name_en": "{name_en}",
        "origin": "待补充",
        "size": "{template['size']}",
        "weight_range": "{template['weight_range']}",
        "height_range": "{template['height_range']}",
        "lifespan": "{template['lifespan']}",
        "personality": {json.dumps(template['personality'], ensure_ascii=False)},
        "coat_color": {json.dumps(template['coat_color'], ensure_ascii=False)},
        "coat_length": "{template['coat_length']}",
        "shedding": "{template['shedding']}",
        "exercise_need": "{template['exercise_need']}",
        "feeding_tips": "{template['feeding_tips']}",
        "forbidden_foods": {json.dumps(template['forbidden_foods'], ensure_ascii=False)},
        "recommended_food": "{template['recommended_food']}",
        "common_diseases": {json.dumps(template['common_diseases'], ensure_ascii=False)},
        "vaccine_schedule": "{template['vaccine_schedule']}",
        "grooming": "{template['grooming']}",
        "tags": ["{template['size']}"],
        "image_url": "",
        "description": "{description}"
    }}'''
    return entry

# 生成所有新条目
new_entries = []
for class_idx_str, breed_id in class_to_breed_id.items():
    class_idx = int(class_idx_str)
    # 只处理新的 breed_id (>= 61)
    if int(breed_id) >= 61:
        entry = generate_breed_entry(breed_id, class_idx)
        new_entries.append(entry)

# 写入文件
output = BACKEND_DIR / "ml" / "new_breeds.txt"
with open(output, "w", encoding="utf-8") as f:
    f.write(",\n".join(new_entries))

print(f"生成了 {len(new_entries)} 个新品种条目 -> {output}")
