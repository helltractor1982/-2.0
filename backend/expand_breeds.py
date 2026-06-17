"""
扩展 breeds_data.py: 60品种 -> 120品种, 添加 synset_id 字段
运行方式: python expand_breeds.py
"""
import re
import json

INPUT_FILE = r'c:\Users\86139\WorkBuddy\2026-05-29-11-15-07\dog-doctor\backend\breeds_data.py'

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# 提取所有现有品种的 breed_id, name_zh, name_en
pattern = r'"breed_id": "(\d+)".*?"name_zh": "([^"]*?)".*?"name_en": "([^"]*?)"'
pairs = re.findall(pattern, content, re.DOTALL)
print(f"Found {len(pairs)} existing breeds")

# 为每个现有品种分配 synset_id (基于名称匹配Stanford Dogs数据集)
# breed_mapping.py 中有完整的120个映射
synset_map = {}

# Stanford Dogs 数据集中的完整 synset 列表(按字母序 = 模型索引序)
ALL_SYNSETS_SORTED = [
    "n02085620","n02085782","n02085936","n02086079","n02086240",
    "n02086646","n02087046","n02087394","n02088094","n02088238",
    "n02088364","n02088466","n02088632","n02089078","n02089867",
    "n02089973","n02090379","n02090622","n02090721","n02091032",
    "n02091134","n02091244","n02091467","n02091635","n02091831",
    "n02092002","n02092339","n02093256","n02093428","n02093647",
    "n02093754","n02093859","n02093991","n02094114","n02094258",
    "n02095314","n02095570","n02095889","n02096051","n02096177",
    "n02096294","n02096437","n02096585","n02097047","n02097130",
    "n02097209","n02097298","n02097474","n02097658","n02098105",
    "n02098286","n02098413","n02099267","n02099429","n02099601",
    "n02099712","n02099849","n02100236","n02100583","n02100735",
    "n02100877","n02101006","n02101388","n02101556","n02102040",
    "n02102177","n02102318","n02102480","n02102973","n02104029",
    "n02104365","n02105056","n02105162","n02105251","n02105412",
    "n02105505","n02105641","n02105855","n02106030","n02106166",
    "n02106382","n02106550","n02106662","n02107142","n02107312",
    "n02107574","n02107683","n02107908","n02108000","n02108089",
    "n02108422","n02108551","n02108915","n02109047","n02109525",
    "n02109961","n02110063","n02110627","n02110806","n02110958",
    "n02111129","n02111277","n02111500","n02111889","n02112018",
    "n02112137","n02112350","n02112706","n02113023","n02113186",
    "n02113624","n02113712","n02113799","n02113978","n02115641",
    "n02115913","n02116738",
]

# 基于英文名匹配的映射表 (用于前60个已有品种)
name_to_synset = {
    'Siberian Husky': 'n02110185',       # 西伯利亚雪橇犬
    'Golden Retriever': 'n02099601',      # 金毛寻回犬
    'Labrador Retriever': 'n02099712',    # 拉布拉多寻回犬
    'German Shepherd': 'n02106662',        # 德国牧羊犬
    'Shiba Inu': 'n02094433',              # 柴犬
    'Border Collie': 'n02106166',          # 边境牧羊犬
    'Poodle': 'n02113799',                 # 贵宾犬(标准)
    'French Bulldog': 'n02108915',         # 法国斗牛犬
    'English Bulldog': 'n02105412',         # 英国斗牛犬
    'Alaskan Malamute': 'n02110063',       # 阿拉斯加雪橇犬
    'Samoyed': 'n02111889',                # 萨摩耶犬
    'Pomeranian': 'n02112018',             # 博美犬
    'Corgi': 'n02113023',                  # 柯基犬(Pembroke)
    'Beagle': 'n02088364',                 # 比格犬
    'Chow Chow': 'n02112137',               # 松狮犬
    'Toy Poodle': 'n02113624',             # 玩具贵宾
    'Maltese dog': 'n02085936',            # 马尔济斯/比熊近似
    'Doberman Pinscher': 'n02107142',     # 杜宾犬
    'Great Dane': 'n02109047',             # 大丹犬
    'Shih Tzu': 'n02086240',               # 西施犬
    'Pug': 'n02110958',                    # 巴哥犬
    'Schnauzer': 'n02097209',              # 标准雪纳瑞
    'Papillon': 'n02086646',              # 蝴蝶犬
    'Yorkshire Terrier': 'n02094433',      # 约克夏梗
    'Irish Setter': 'n02100877',           # 爱尔兰赛特犬
    'Bloodhound': 'n02088466',             # 寻血猎犬
}

# 分配前60个品种的 synset
used_synsets = set()
for bid, zh, en in pairs:
    en_clean = en.strip() if en else ""
    best_match = None
    for name_key, synset in name_to_synset.items():
        if name_key.lower() in en_clean.lower() or en_clean.lower() in name_key.lower():
            best_match = synset
            break
    if best_match and best_match not in used_synsets:
        synset_map[bid] = best_match
        used_synsets.add(best_match)
    else:
        # 未匹配到的分配剩余 synset (按顺序)
        for s in ALL_SYNSETS_SORTED:
            if s not in used_synsets:
                synset_map[bid] = s
                used_synsets.add(s)
                break

print(f"Assigned synset IDs to {len(synset_map)}/60 existing breeds")

# ---- 策略: 在每个品种字典中添加 synset_id 字段 ----
def add_synset_to_breed(match):
    """在品种字典末尾、description字段之前插入 synset_id"""
    bid = match.group(1)
    sid = synset_map.get(bid, "")
    # 找到 "description" 字段的起始位置并在其前面插入
    desc_match = re.search(r'(\s+"description":)', match.string[match.end():match.end()+200] if False else ...)
    if desc_match is None:
        # 如果找不到 description, 就在 } 前面插入
        insert_pos = match.end() + match.string[match.end():].find('\n    },')
    else:
        insert_pos = match.end() + match.string[match.end():desc_match.start()]
    return match.string[:match.end()] + f',\n        "synset_id": "{sid}"' + match.string[match.end():]

# 更简单的方法: 直接在每个品种块的最后 } 之前添加 synset_id
# 使用正则在 }, 前插入

# 实际最简单的方式: 全局替换
# 每个 breed 字典的格式是固定的, 我们可以找到模式并替换

new_lines = []
in_list = False
brace_depth = 0
current_bid = None
need_synset = set(str(i).zfill(3) for i in range(1, 61))

lines = content.split('\n')
for i, line in enumerate(lines):
    new_lines.append(line)

    # 检测是否进入 BREEDS_DATA 列表
    if 'BREEDS_DATA = [' in line:
        in_list = True
        continue

    # 检测 breed_id 行
    bid_match = re.match(r'\s*"breed_id": "(\d+)", line)
    if bid_match and in_list:
        current_bid = bid_match.group(1)

    # 在 description 字段之前插入 synset_id
    if current_bid and current_bid in need_synset and '"description":' in line and in_list:
        sid = synset_map.get(current_bid, '')
        indent = len(line) - len(line.lstrip())
        new_lines.append(f'{indent * " "}"synset_id": "{sid}",')
        need_synset.discard(current_bid)

content_out = '\n'.join(new_lines)

# ---- Step 2: 追加新的 60 个品种 (ID 061-120) ----
# 这些品种来自 Stanford Dogs Dataset 但不在原有60个中

stanford_new_breeds_info = [
    # (bid, zh, en, origin, size, weight, height, lifespan, synset)
    ("061", "吉娃娃", "Chihuahua", "墨西哥", "超小型犬", "1-3 kg", "15-23 cm", "14-20年", "n02085620"),
    ("062", "日本狆", "Japanese Spaniel", "日本", "小型犬", "5-7 kg", "23-30 cm", "12-14年", "n02085782"),
    ("063", "马尔济斯犬", "Maltese Dog", "地中海", "玩具犬", "2-4 kg", "20-25 cm", "12-16年", "n02085936"),
    ("064", "北京犬", "Pekinese", "中国", "小型犬", "3-6 kg", "18-22 cm", "12-14年", "n02086079"),
    ("065", "布伦海姆猎犬", "Blenheim Spaniel", "英国", "中大型犬", "8-16 kg", "33-43 cm", "10-14年", "n02086646"),
    ("066", "曼彻斯特梗", "Manchester Terrier", "英国", "小型犬", "5-7 kg", "25-30 cm", "14-16年", "n02087046"),
    ("067", "罗得西亚背脊犬", "Rhodesian Ridgeback", "非洲南部", "大型犬", "27-32 kg", "61-69 cm", "10-12年", "n02087394"),
    ("068", "阿富汗猎犬", "Afghan Hound", "阿富汗", "大型犬", "23-29 kg", "68-74 cm", "12-15年", "n02088094"),
    ("069", "巴吉度猎犬", "Basset Hound", "法国", "中型犬", "20-30 kg", "33-40 cm", "10-12年", "n02088238"),
    ("070", "比格犬(标准)", "Beagle (Standard)", "英国", "中大型犬", "9-11 kg", "33-41 cm", "12-15年", "n02088364"),
    ("071", "寻血猎犬", "Bloodhound", "比利时", "大型犬", "36-50 kg", "58-69 cm", "7-10年", "n02088466"),
    ("072", "蓝斑猎浣熊犬", "Bluetick Coonhound", "美国", "大型犬", "20-32 kg", "53-64 cm", "10-14年", "n02088632"),
    ("073", "黑棕浣熊犬", "Black & Tan Coonhound", "美国", "大型犬", "25-34 kg", "56-64 cm", "10-13年", "n02089078"),
    ("074", "沃克猎浣熊犬", "Walker Hound", "美国", "大型犬", "23-32 kg", "53-63 cm", "11-14年", "n02089867"),
    ("075", "英国猎狐犬", "English Foxhound", "英国", "大型犬", "27-34 kg", "61-72 cm", "10-13年", "n02089973"),
    ("076", "红骨猎犬", "Redbone Coonhound", "美国", "中大型犬", "20-28 kg", "48-56 cm", "10-14年", "n02090379"),
    ("077", "波索尔犬", "Borzoi", "俄罗斯", "大型犬", "27-42 kg="71-86 cm", "9-12年", "n02090622"),
    ("078", "爱尔兰猎狼犬", "Irish Wolfhound", "爱尔兰", "超大型犬", "45-70 kg", "71-86 cm", "6-8年", "n02090721"),
    ("079", "意大利灵缇", "Italian Greyhound", "意大利", "中大型犬", "3-7 kg", "33-43 cm", "9-15年", "n02091032"),
    ("080", "惠比特犬", "Whippet", "英国", "中型犬", "10-18 kg", "44-57 cm", "12-15年", "n02091134"),
    ("081", "伊比赞猎犬", "Ibizan Hound", "西班牙", "大型犬", "22-29 kg", "56-74 cm", "11-14年", "n02091244"),
    ("082", "挪威猎麋犬", "Norwegian Elkhound", "挪威", "中型犬", "20-27 kg": "44-52 cm", "11-14年", "n02091467"),
    ("083", "水獭猎犬", "Otterhound", "英国", "大型犬", "30-40 kg", "61-69 cm", "10-13年", "n02091635"),
    ("084", "萨路基猎犬", "Saluki", "中东", "大型犬", "18-27 kg", "58-71 cm", "12-14年", "n02091831"),
    ("085", "苏格兰鹿犬", "Scottish Deerhound", "苏格兰", "超大型犬", "34-50 cm": "71-82 cm", "8-11年", "n02092002"),
    ("086", "威玛犬", "Weimaraner", "德国", "大型犬", "25-34 kg", "58-70 cm", "10-13年", "n02092339"),
    ("087", "斯塔福郡斗牛梗", "Staffordshire Bull Terrier", "英国", "中型犬", "11-17 kg", "35-41 cm", "10-14年", "n02093256"),
    ("088", "美国斯塔福郡梗", "American Staffordshire Terrier", "美国", "中型犬", "25-32 cm": "43-49 cm", "11-14年", "n02093428"),
    ("089", "贝灵顿梗", "Bedlington Terrier", "英国", "中大型犬", "8-11 kg", "38-44 cm", "12-14年", "n02093647"),
    ("090", "边境梗", "Border Terrier", "英国", "小型犬", "5.5-7 kg", "25-30 cm", "12-15年", "n02093754"),
    ("091", "凯利蓝梗", "Kerry Blue Terrier", "爱尔兰", "中型犬", "15-18 kg": "44-50 cm", "12-15年", "n02093859"),
    ("092", "爱尔兰梗", "Irish Terrier", "爱尔兰", "中型犬", "11-14 kg": "43-48 cm", "12-16年", "n02093991"),
    ("093", "诺福克梗", "Norfolk Terrier", "英国", "小型犬", "5-6 kg": "23-26 cm", "12-15年", "n02094114"),
    ("094", "诺里奇梗", "Norwich Terrier", "英国", "小型犬", "5-6 kg": "24-27 cm", "12-15年", "n02094258"),
    ("095", "约克夏梗", "Yorkshire Terrier", "英国", "小型犬", "2-3.5 kg", "15-23 cm", "12-16年", "n02094433"),
    ("096", "刚毛猎狐梗", "Wire Fox Terrier", "英国", "小型犬", "6.5-9 kg": "34-40 cm", "10-14年", "n02095314"),
    ("097", "莱克兰梗", "Lakeland Terrier", "英国", "小型犬": "6-8 kg": "33-38 cm", "10-14年", "n02095570"),
    ("098", "西里汉姆梗", "Sealyham Terrier", "威尔士", "小型犬": "8.5-9 kg": "25-30 cm": "12-15年", "n02095889"),
    ("099", "万能梗", "Airedale Terrier", "英国", "中大型犬": "20-30 kg": "56-62 cm": "8-10年", "n02096051"),
    ("100", "凯恩梗", "Cairn Terrier", "苏格兰", "小型犬": "6-8 kg": "25-31 cm": "12-15年", "n02096177"),
    ("101", "澳大利亚梗", "Australian Terrier", "澳大利亚", "小型犬": "5.5-7 kg": "24-28 cm": "12-15年", "n02096294"),
    ("102", "丹迪丁蒙梗", "Dandie Dinmont Terrier", "苏格兰", "小型犬": "8-11 kg": "20-28 cm": "11-14年", "n02096437"),
    ("103", "波士顿梗", "Boston Terrier", "美国", "中型犬": "5-11 kg": "38-43 cm": "11-15年", "n02096585"),
    ("104", "迷你雪纳瑞", "Miniature Schnauzer", "德国", "小型犬": "5-9 kg": "30-36 cm": "12-15年", "n02097047"),
    ("105", "巨型雪纳瑞", "Giant Schnauzer", "德国", "大型犬": "27-41 cm": "59-70 cm": "10-12年", "n02097130"),
    ("106", "标准雪纳瑞", "Standard Schnauzer", "德国": "中大型犬": "14-20 cm": "45-50 cm": "12-15年", "n02097209"),
    ("107", "苏格兰梗", "Scottish Terrier", "苏格兰", "小型犬": "8-10 kg": "25-28 cm": "11-14年", "n02097298"),
    ("108", "西藏梗", "Tibetan Terrier", "中国西藏", "中型犬": "8-12 kg": "33-41 cm": "12-15年", "n02097474"),
    ("109", "丝毛梗", "Silky Terrier", "澳大利亚", "小型犬": "3.5-5 kg": "20-25 cm": "12-15年", "n02097658"),
    ("110", "软麦色梗", "Soft-Coated Wheaten Terrier", "爱尔兰", "中型犬": "14-18 kg": "42-46 cm": "12-14年", "n02098105"),
    ("111", "西高地白梗", "West Highland White Terrier", "苏格兰", "小型犬": "6-9 kg": "25-28 cm": "12-15年", "n02098286"),
    ("112", "拉萨犬", "Lhasa Apso", "中国西藏", "中小型犬": "5-7 kg": "25-28 cm": "12-16年", "n02098413"),
    ("113", "平毛寻回犬", "Flat-Coated Retriever", "英国", "大型犬": "23-32 kg": "55-62 cm": "10-12年", "n02099267"),
    ("114", "卷毛寻回犬", "Curly-Coated Retriever", "英国", "大型犬": "25-36 kg": "56-62 cm": "10-12年", "n02099429"),
    ("115", "切萨皮克湾寻回犬", "Chesapeake Bay Retriever", "美国", "大型犬": "25-36 kg": "53-66 cm": "10-13年", "n02099849"),
    ("116", "德国短毛指示犬", "German Shorthaired Pointer", "德国", "大型犬": "20-30 kg": "53-64 cm": "10-13年", "n02100236"),
    ("117", "维兹拉犬", "Vizsla", "匈牙利", "中大型犬": "20-27 kg": "54-61 cm": "10-14年", "n02100583"),
    ("118", "英国塞特犬", "English Setter", "英格兰", "大型犬": "25-30 kg": "61-69 cm": "10-12年", "n02100735"),
    ("119", "爱尔兰塞特犬", "Irish Setter", "爱尔兰", "大型犬": "25-32 kg": "58-68 cm": "11-15年", "n02100877"),
    ("120", "戈登塞特犬", "Gordon Setter", "苏格兰", "大型犬": "20-32 kg": "58-69 cm": "10-12年", "n02101006"),
]

# 构建60个新品种条目文本
new_breeds_text = []
for info in stanford_new_breeds_info:
    bid, zh, en, origin, size, wh, ht, ls, synset = info
    breed_entry = f'''    {{
        "breed_id": "{bid}",
        "name_zh": "{zh}",
        "name_en": "{en}",
        "origin": "{origin}",
        "size": "{size}",
        "weight_range": "{wh}",
        "height_range": "{ht}",
        "lifespan": "{ls}",
        "personality": ["聪明", "忠诚", "友善", "活泼"],
        "coat_color": ["多种颜色"],
        "coat_length": "多变",
        "shedding": "中",
        "exercise_need": "中等",
        "feeding_tips": "每日进食适量，注意营养均衡，选择适合体型的高质量犬粮",
        "forbidden_foods": ["葡萄", "巧克力", "洋葱"],
        "recommended_food": "优质全价犬粮",
        "common_diseases": ["髋关节发育不良", "眼部疾病", "皮肤病"],
        "vaccine_schedule": "幼犬6-8周首免，每年加强接种",
        "grooming": "定期梳毛和洗澡，保持清洁健康",
        "tags": ["{size}", "伴侣犬", "聪明", "友好"],
        "image_url": "",
        "description": "{zh}({en})是一种{size}犬种，性格温和友善，是优秀的家庭伴侣犬。",
        "synset_id": "{synset}"
    }},'''
    new_breeds_text.append(breed_entry)

# 将新品种插入到列表结束符 ] 之前
insert_marker = '\n]'
if insert_marker in content_out:
    parts = content_out.rsplit(insert_marker, 1)
    content_out = parts[0] + ',\n' + ',\n'.join(new_breeds_text) + '\n]' + parts[1]
else print("WARNING: Could not find list end marker!")

# 写回文件
with open(INPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(content_out)

print(f"\nDone! File written back to {INPUT_FILE}")
print(f"Total breeds now: {len(pairs) + len(stanford_new_breeds_info)}")
