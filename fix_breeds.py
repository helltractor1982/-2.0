#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_breeds.py - Remap breed names to match class_names.json order.
Reads breeds_data.py (original Python source), applies name mappings,
splits, and adds new entries.
Outputs exactly 120 entries matching class_names.json as JS.
"""

import json
import re
import os
import sys
import io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Paths
CLASS_NAMES_PATH = r"D:\dog-doctor\backend\ml\models\class_names.json"
BREEDS_DATA_PATH = r"D:\dog-doctor\backend\breeds_data.py"
OUTPUT_JS_PATH = r"C:\Users\86139\WorkBuddy\2026-05-30-12-43-03\breeds_generated.js"

# ─── Load class_names.json ───
with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
    class_names = json.load(f)

print(f"class_names.json: {len(class_names)} breeds")

# ─── Load breeds_data.py via exec ───
with open(BREEDS_DATA_PATH, "r", encoding="utf-8") as f:
    source = f.read()

# Execute in a clean namespace to get BREEDS_DATA
ns = {}
exec(source, ns)
BREEDS_DATA = ns["BREEDS_DATA"]

# Build lookup by name_zh
breed_data = {}
for item in BREEDS_DATA:
    zh = item.get("name_zh", "")
    if zh and zh not in breed_data:
        # Convert to the JS format dict
        coat_colors = item.get("coat_color", [])
        coat_length = item.get("coat_length", "")
        coat = coat_length + "/" + "+".join(coat_colors) if coat_colors else coat_length

        breed_data[zh] = {
            "zh": zh,
            "en": item.get("name_en", ""),
            "origin": item.get("origin", ""),
            "size": item.get("size", ""),
            "weight": item.get("weight_range", ""),
            "height": item.get("height_range", ""),
            "lifespan": item.get("lifespan", ""),
            "shedding": item.get("shedding", ""),
            "exercise": item.get("exercise_need", ""),
            "coat": coat,
            "personality": item.get("personality", []),
            "tags": item.get("tags", []),
            "diseases": item.get("common_diseases", []),
            "grooming": item.get("grooming", ""),
            "feeding": item.get("feeding_tips", ""),
            "vaccine": item.get("vaccine_schedule", ""),
            "forbidden": item.get("forbidden_foods", []),
            "emoji": item.get("emoji", "🐕"),
            "desc": item.get("description", ""),
        }

print(f"Loaded {len(breed_data)} unique breeds from breeds_data.py")

# ─── Name mapping: current zh name -> class_names.json name ───
RENAME_MAP = {
    "苏格兰牧羊犬": "柯利牧羊犬",
    "西藏獒": "藏獒",
    "威玛犬": "威玛猎犬",
    "布列塔尼猎犬": "布列塔尼犬",
    "巴仙吉犬": "巴辛吉犬",
    "猎狐梗": "刚毛猎狐梗",
    "马里诺斯犬": "比利时马林诺斯犬",
    "卡迪根威尔士柯基": "卡迪根威尔士柯基犬",
    "巴塞特猎犬": "巴吉度猎犬",
    "爱尔兰赛特犬": "爱尔兰雪达犬",
    "沃克猎犬": "步行猎犬",
    "泰迪犬（玩具贵宾）": "玩具贵宾犬",
    "柯基犬": "彭布罗克威尔士柯基犬",
    "雪纳瑞": "迷你雪纳瑞",
}

# ─── Split: 贵宾犬 -> 迷你贵宾犬 + 标准贵宾犬 (泰迪 covers 玩具贵宾犬) ───
SPLIT_EXTRA = {
    "迷你贵宾犬": {
        "zh": "迷你贵宾犬", "en": "Miniature Poodle", "origin": "法国/德国",
        "size": "小型犬", "weight": "5-8 kg", "height": "28-35 cm",
        "lifespan": "13-16年", "shedding": "极低", "exercise": "中高",
        "coat": "卷曲/黑+白+棕色",
        "personality": ["聪明", "活泼", "友善", "适应性强"],
        "tags": ["小型犬", "非运动犬", "低掉毛", "适合过敏者", "聪明"],
        "diseases": ["髌骨脱位", "渐进性视网膜萎缩", "牙齿问题"],
        "grooming": "每6-8周专业美容修剪，每周梳毛",
        "feeding": "每日进食量约120-160g",
        "vaccine": "标准程序，每年加强",
        "forbidden": ["葡萄", "巧克力", "咖啡因"],
        "emoji": "🐕",
        "desc": "迷你贵宾犬是贵宾犬家族中的中等体型成员，聪明活泼，几乎不掉毛，是非常受欢迎的城市伴侣犬。",
    },
    "标准贵宾犬": {
        "zh": "标准贵宾犬", "en": "Standard Poodle", "origin": "法国/德国",
        "size": "大型犬", "weight": "20-32 kg", "height": "38-60 cm",
        "lifespan": "12-15年", "shedding": "极低", "exercise": "高",
        "coat": "卷曲/黑+白+棕色",
        "personality": ["聪明", "优雅", "活泼", "忠诚"],
        "tags": ["大型犬", "运动犬", "低掉毛", "适合过敏者", "最聪明犬种之一"],
        "diseases": ["髋关节发育不良", "胃扭转", "肾上腺功能减退", "癫痫"],
        "grooming": "每6-8周专业美容修剪，每周梳毛",
        "feeding": "每日进食量约300-400g",
        "vaccine": "标准程序，每年加强",
        "forbidden": ["葡萄", "巧克力", "咖啡因"],
        "emoji": "🐕",
        "desc": "标准贵宾犬是贵宾犬家族中最古老的原始成员，智商在所有犬种中排名第二，优雅而聪明。",
    },
}

# ─── New entries for breeds completely missing from data ───
NEW_BREEDS = {
    "威尔士激飞猎犬": {
        "zh": "威尔士激飞猎犬", "en": "Welsh Springer Spaniel", "origin": "英国威尔士",
        "size": "中型犬", "weight": "16-20 kg", "height": "46-48 cm", "lifespan": "12-15年",
        "shedding": "中", "exercise": "高", "coat": "中长波浪/红白",
        "personality": ["活泼开朗", "忠诚友善", "工作热情", "亲人"],
        "tags": ["中型犬", "猎犬", "红白毛色"],
        "diseases": ["髋关节发育不良", "眼部疾病", "耳部感染"],
        "grooming": "每周梳毛2-3次，定期清洁耳朵", "feeding": "每日2次，适量运动",
        "vaccine": "标准接种程序", "forbidden": ["巧克力", "葡萄"],
        "emoji": "🐕", "desc": "威尔士激飞猎犬以其独特的红白毛色著称，是出色的猎鸟犬和家庭伴侣犬。",
    },
    "大瑞士山地犬": {
        "zh": "大瑞士山地犬", "en": "Greater Swiss Mountain Dog", "origin": "瑞士",
        "size": "超大型犬", "weight": "59-61 kg", "height": "60-72 cm", "lifespan": "8-11年",
        "shedding": "高", "exercise": "中高", "coat": "短厚双层/黑底+棕白斑",
        "personality": ["忠诚护主", "温和友善", "勇敢自信", "活泼"],
        "tags": ["超大型犬", "工作犬", "瑞士犬"],
        "diseases": ["髋关节发育不良", "胃扭转", "眼科疾病"],
        "grooming": "每周梳毛2-3次", "feeding": "每日2次大型犬粮",
        "vaccine": "标准接种程序", "forbidden": ["巧克力", "葡萄"],
        "emoji": "🐕", "desc": "大瑞士山地犬是瑞士山地犬中体型最大的，曾是农场多面手，性格忠诚温和。",
    },
    "伯恩山犬": {
        "zh": "伯恩山犬", "en": "Bernese Mountain Dog", "origin": "瑞士伯尔尼",
        "size": "超大型犬", "weight": "36-54 kg", "height": "58-70 cm", "lifespan": "7-10年",
        "shedding": "高", "exercise": "中", "coat": "长厚双层/黑底+棕白三色",
        "personality": ["温柔友善", "忠诚可靠", "耐心温和", "爱孩子"],
        "tags": ["超大型犬", "工作犬", "三色", "瑞士犬"],
        "diseases": ["癌症（高发）", "髋关节发育不良", "肘关节发育不良", "胃扭转"],
        "grooming": "每周梳毛3-4次，换毛期每天", "feeding": "每日2次大型犬粮，注意体重控制",
        "vaccine": "标准接种程序", "forbidden": ["巧克力", "葡萄", "洋葱"],
        "emoji": "🐕", "desc": "伯恩山犬以其经典的三色被毛和温柔的性格著称，是非常好的家庭犬，但寿命较短。",
    },
    "阿彭策尔山犬": {
        "zh": "阿彭策尔山犬", "en": "Appenzeller Sennenhund", "origin": "瑞士",
        "size": "中型犬", "weight": "22-32 kg", "height": "47-58 cm", "lifespan": "12-14年",
        "shedding": "中", "exercise": "高", "coat": "短双层/黑底+棕白斑",
        "personality": ["活泼机警", "勇敢忠诚", "聪明好学", "精力充沛"],
        "tags": ["中型犬", "牧羊犬", "瑞士犬"],
        "diseases": ["髋关节发育不良", "眼科疾病"],
        "grooming": "每周梳毛2次", "feeding": "每日2次，高蛋白粮",
        "vaccine": "标准接种程序", "forbidden": ["巧克力", "葡萄"],
        "emoji": "🐕", "desc": "阿彭策尔山犬是瑞士四种山地犬之一，以高额头上的独特斑纹和活泼的性格著称。",
    },
    "恩特雷布赫山地犬": {
        "zh": "恩特雷布赫山地犬", "en": "Entlebucher Mountain Dog", "origin": "瑞士",
        "size": "中型犬", "weight": "20-30 kg", "height": "44-50 cm", "lifespan": "11-15年",
        "shedding": "中", "exercise": "高", "coat": "短双层/黑底+棕黄白斑",
        "personality": ["活泼机警", "忠诚可靠", "勇敢自信", "聪明"],
        "tags": ["中型犬", "牧羊犬", "瑞士犬", "稀有"],
        "diseases": ["髋关节发育不良", "眼科疾病"],
        "grooming": "每周梳毛2次", "feeding": "每日2次中型犬粮",
        "vaccine": "标准接种程序", "forbidden": ["巧克力", "葡萄"],
        "emoji": "🐕", "desc": "恩特雷布赫山地犬是瑞士山地犬中最小的品种，曾是牧牛犬，性格活泼忠诚。",
    },
    "拳师犬": {
        "zh": "拳师犬", "en": "Boxer", "origin": "德国",
        "size": "大型犬", "weight": "25-34 kg", "height": "53-63 cm", "lifespan": "10-12年",
        "shedding": "中", "exercise": "高", "coat": "短光滑/浅黄褐色+虎斑",
        "personality": ["活泼好动", "忠诚护主", "友善温柔", "聪明"],
        "tags": ["大型犬", "工作犬", "家庭犬"],
        "diseases": ["癌症", "心脏病", "髋关节发育不良", "甲状腺功能减退"],
        "grooming": "每周梳毛1次，每月洗澡", "feeding": "每日2次大型犬粮",
        "vaccine": "标准接种程序", "forbidden": ["巧克力", "葡萄", "洋葱"],
        "emoji": "🥊", "desc": "拳师犬是德国培育的优秀工作犬，外表强壮但性格极其温柔，尤其喜爱儿童。",
    },
    "斗牛獒犬": {
        "zh": "斗牛獒犬", "en": "Bullmastiff", "origin": "英国",
        "size": "超大型犬", "weight": "45-59 kg", "height": "61-68 cm", "lifespan": "8-10年",
        "shedding": "中", "exercise": "中", "coat": "短/浅黄褐色+虎斑+红色",
        "personality": ["忠诚护主", "冷静沉稳", "勇敢无畏", "温和"],
        "tags": ["超大型犬", "工作犬", "护卫犬"],
        "diseases": ["髋关节发育不良", "胃扭转", "眼部疾病", "心脏病"],
        "grooming": "每周梳毛1次，每月洗澡", "feeding": "每日2次大型犬粮，注意防止胃扭转",
        "vaccine": "标准接种程序", "forbidden": ["巧克力", "葡萄"],
        "emoji": "🐕", "desc": "斗牛獒犬是由斗牛犬和獒犬杂交培育的护卫犬，天生的守护者，忠诚且强壮。",
    },
    "圣伯纳犬": {
        "zh": "圣伯纳犬", "en": "St. Bernard", "origin": "瑞士",
        "size": "超大型犬", "weight": "64-120 kg", "height": "65-90 cm", "lifespan": "8-10年",
        "shedding": "高", "exercise": "低中", "coat": "长/短（两种）/白红+白棕",
        "personality": ["温柔友善", "耐心忠诚", "冷静沉稳", "爱孩子"],
        "tags": ["超大型犬", "工作犬", "救援犬"],
        "diseases": ["髋关节发育不良", "胃扭转", "心脏病", "眼部疾病"],
        "grooming": "每周梳毛3-4次，长毛型需更频繁", "feeding": "每日2次大型犬粮，严格控制体重",
        "vaccine": "标准接种程序", "forbidden": ["巧克力", "葡萄"],
        "emoji": "🏔️", "desc": "圣伯纳犬以阿尔卑斯山雪地救援闻名，是世界上最著名的救援犬种之一。",
    },
    "猴面犬": {
        "zh": "猴面犬", "en": "Affenpinscher", "origin": "德国",
        "size": "超小型犬", "weight": "3-4 kg", "height": "23-30 cm", "lifespan": "12-15年",
        "shedding": "低", "exercise": "中", "coat": "粗糙硬毛/黑色+灰色",
        "personality": ["好奇好动", "勇敢自信", "活泼顽皮", "聪明"],
        "tags": ["超小型犬", "玩具犬", "猴脸"],
        "diseases": ["膝关节脱位", "呼吸道问题", "骨折"],
        "grooming": "每周梳毛2次，定期修剪", "feeding": "每日2次，少量多餐",
        "vaccine": "标准接种程序", "forbidden": ["巧克力", "葡萄"],
        "emoji": "🐵", "desc": "猴面犬因面部特征酷似猴子而得名，是活泼勇敢的小型玩具犬。",
    },
    "莱昂贝格犬": {
        "zh": "莱昂贝格犬", "en": "Leonberger", "origin": "德国",
        "size": "超大型犬", "weight": "45-77 kg", "height": "65-80 cm", "lifespan": "8-10年",
        "shedding": "高", "exercise": "中高", "coat": "长厚双层/金棕色+黑面罩",
        "personality": ["温和友善", "忠诚护主", "冷静沉稳", "爱水"],
        "tags": ["超大型犬", "工作犬", "狮子般外貌"],
        "diseases": ["髋关节发育不良", "骨肉瘤", "胃扭转"],
        "grooming": "每周梳毛3-4次，换毛期每天", "feeding": "每日2次大型犬粮",
        "vaccine": "标准接种程序", "forbidden": ["巧克力", "葡萄"],
        "emoji": "🦁", "desc": "莱昂贝格犬因外貌酷似狮子而得名，是优雅温柔的超大型伴侣犬。",
    },
    "荷兰毛狮犬": {
        "zh": "荷兰毛狮犬", "en": "Keeshond", "origin": "荷兰",
        "size": "中型犬", "weight": "16-18 kg", "height": "43-46 cm", "lifespan": "12-15年",
        "shedding": "高", "exercise": "中", "coat": "厚双层/灰黑+狼灰色+浅色下毛",
        "personality": ["活泼友善", "聪明好学", "忠诚警觉", "爱叫"],
        "tags": ["中型犬", "工作犬", "荷兰国犬"],
        "diseases": ["髋关节发育不良", "糖尿病", "眼科疾病"],
        "grooming": "每周梳毛3次，换毛期每天", "feeding": "每日2次中型犬粮",
        "vaccine": "标准接种程序", "forbidden": ["巧克力", "葡萄"],
        "emoji": "🐕", "desc": "荷兰毛狮犬是荷兰的国犬，以其标志性的眼镜状面部斑纹和蓬松的被毛著称。",
    },
    "墨西哥无毛犬": {
        "zh": "墨西哥无毛犬", "en": "Xoloitzcuintli", "origin": "墨西哥",
        "size": "中型犬", "weight": "9-14 kg", "height": "38-55 cm", "lifespan": "13-18年",
        "shedding": "极低", "exercise": "中", "coat": "无毛/少量短毛/黑色+灰色",
        "personality": ["忠诚警觉", "聪明活泼", "独立", "安静"],
        "tags": ["中型犬", "原始犬", "无毛", "古老犬种"],
        "diseases": ["皮肤问题（晒伤/冻伤）", "牙齿问题"],
        "grooming": "定期清洁皮肤，涂抹防晒霜，注意保暖", "feeding": "每日2次中型犬粮",
        "vaccine": "标准接种程序", "forbidden": ["巧克力", "葡萄"],
        "emoji": "🐕", "desc": "墨西哥无毛犬是阿兹特克文明的神圣犬种，无毛外表独特，性格忠诚安静。",
    },
    "澳洲野犬": {
        "zh": "澳洲野犬", "en": "Dingo", "origin": "澳大利亚",
        "size": "中型犬", "weight": "13-20 kg", "height": "47-60 cm", "lifespan": "10-14年",
        "shedding": "中", "exercise": "极高", "coat": "短双层/黄棕色+黑色",
        "personality": ["独立", "警觉", "野性强", "聪明"],
        "tags": ["中型犬", "原始犬", "野生", "澳大利亚"],
        "diseases": ["相对健康", "寄生虫"],
        "grooming": "每月洗澡，定期驱虫", "feeding": "每日2次，需要高蛋白饮食",
        "vaccine": "狂犬疫苗+综合疫苗", "forbidden": ["巧克力", "葡萄"],
        "emoji": "🐺", "desc": "澳洲野犬是澳大利亚的野生犬种，是最古老的犬种之一，保留了强烈的野性本能。",
    },
    "豺犬": {
        "zh": "豺犬", "en": "Dhole", "origin": "亚洲",
        "size": "中型犬", "weight": "10-20 kg", "height": "42-55 cm", "lifespan": "10-13年",
        "shedding": "中", "exercise": "极高", "coat": "短双层/红棕色+黄棕色",
        "personality": ["群居性强", "聪明", "活跃", "善于狩猎"],
        "tags": ["中型犬", "原始犬", "群居", "野生"],
        "diseases": ["相对健康", "犬瘟热（野生群体）"],
        "grooming": "定期梳理", "feeding": "需要高蛋白肉食",
        "vaccine": "狂犬疫苗", "forbidden": ["巧克力"],
        "emoji": "🐕", "desc": "豺犬是亚洲的野生犬科动物，群居生活，以卓越的团队协作狩猎能力著称。",
    },
    "非洲猎犬": {
        "zh": "非洲猎犬", "en": "African Wild Dog", "origin": "非洲",
        "size": "中型犬", "weight": "18-36 kg", "height": "60-75 cm", "lifespan": "10-12年",
        "shedding": "低", "exercise": "极高", "coat": "短/黑棕+黄+白色斑块",
        "personality": ["群居性强", "合作精神", "聪明", "活跃"],
        "tags": ["中型犬", "原始犬", "群居", "濒危物种"],
        "diseases": ["狂犬病", "犬瘟热（野生群体）"],
        "grooming": "定期梳理", "feeding": "需要大量肉类食物",
        "vaccine": "狂犬疫苗", "forbidden": ["巧克力"],
        "emoji": "🐕", "desc": "非洲猎犬（非洲野犬）是非洲最具社会性的猎食者，以其独特的杂色被毛和高效的群体狩猎闻名。",
    },
}

print(f"New breeds to create: {len(NEW_BREEDS)}")
print(f"Split extra entries: {list(SPLIT_EXTRA.keys())}")


def dict_to_js(d, idx):
    """Convert a breed dict to JS string with 3-digit ID."""
    id_str = f"{idx + 1:03d}"
    d["id"] = id_str
    keys_order = ["id", "zh", "en", "origin", "size", "weight", "height",
                  "lifespan", "shedding", "exercise", "coat", "personality",
                  "tags", "diseases", "grooming", "feeding", "vaccine",
                  "forbidden", "emoji", "desc"]
    parts = []
    for key in keys_order:
        val = d.get(key, "")
        if isinstance(val, list):
            js_val = '["' + '","'.join(
                str(v).replace('\\', '\\\\').replace('"', '\\"') for v in val
            ) + '"]'
        else:
            val_s = str(val).replace('\\', '\\\\').replace('"', '\\"')
            js_val = f'"{val_s}"'
        parts.append(f'{key}:{js_val}')
    return "  { " + ", ".join(parts) + " }"


# ─── Build final output ───
used_sources = set()
output_lines = []
not_found = []

for i, cn_name in enumerate(class_names):
    # 1. Direct match: breed zh name == class_name
    if cn_name in breed_data and cn_name not in used_sources:
        d = dict(breed_data[cn_name])
        used_sources.add(cn_name)
        output_lines.append(dict_to_js(d, i))
        continue

    # 2. Check rename map
    found = False
    for src, target in RENAME_MAP.items():
        if target == cn_name and src in breed_data and src not in used_sources:
            d = dict(breed_data[src])
            d["zh"] = cn_name
            if src == "泰迪犬（玩具贵宾）":
                d["en"] = "Toy Poodle"
            elif src == "柯基犬":
                d["en"] = "Pembroke Welsh Corgi"
                d["desc"] = "彭布罗克威尔士柯基犬是最受欢迎的柯基品种，因英国女王喜爱而闻名，短腿长身，聪明友善。"
            elif src == "雪纳瑞":
                d["en"] = "Miniature Schnauzer"
                d["size"] = "小型犬"
                d["weight"] = "5-9 kg"
                d["height"] = "30-36 cm"
                d["desc"] = "迷你雪纳瑞是雪纳瑞家族中最受欢迎的成员，以其标志性的胡须和眉毛著称，聪明活泼。"
            used_sources.add(src)
            output_lines.append(dict_to_js(d, i))
            found = True
            break
    if found:
        continue

    # 3. Check split extra (from 贵宾犬)
    if cn_name in SPLIT_EXTRA:
        d = dict(SPLIT_EXTRA[cn_name])
        output_lines.append(dict_to_js(d, i))
        continue

    # 4. Check new breeds
    if cn_name in NEW_BREEDS:
        d = dict(NEW_BREEDS[cn_name])
        output_lines.append(dict_to_js(d, i))
        continue

    # 5. Not found
    not_found.append(cn_name)
    print(f"  WARNING: No data for '{cn_name}' (index {i})")

print(f"\nOutput entries: {len(output_lines)}")
print(f"Not found: {not_found}")

if not_found:
    print("ERROR: Some breeds could not be mapped!")
    sys.exit(1)

# ─── Write output ───
output_content = "const BREEDS = [\n" + ",\n".join(output_lines) + "\n];"

with open(OUTPUT_JS_PATH, "w", encoding="utf-8") as f:
    f.write(output_content)

print(f"\nSuccessfully wrote {len(output_lines)} breeds to {OUTPUT_JS_PATH}")

# Verify
with open(OUTPUT_JS_PATH, "r", encoding="utf-8") as f:
    verify = f.read()

# Count entries by id pattern
ids = re.findall(r'id:"(\d+)"', verify)
print(f"Verify: {len(ids)} entries in output")

# Verify all class_names are present
output_zh = re.findall(r'zh:"([^"]+)"', verify)
missing_in_output = [cn for cn in class_names if cn not in output_zh]
extra_in_output = [zh for zh in output_zh if zh not in class_names]
print(f"Missing from output: {missing_in_output}")
print(f"Extra in output: {extra_in_output}")
print(f"Output zh count: {len(output_zh)}, class_names count: {len(class_names)}")

# Verify IDs are sequential 3-digit
expected_ids = [f"{i+1:03d}" for i in range(120)]
print(f"IDs match expected: {ids == expected_ids}")
