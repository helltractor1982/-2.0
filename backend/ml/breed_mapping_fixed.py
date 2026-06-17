"""
犬种映射表: custom breed_id ↔ Stanford synset_id ↔ class_idx
覆盖 Stanford Dogs Dataset 全部 120 个品种
"""

# 按 synset_id 排序的 120 品种映射
BREED_MAP: list[dict] = [
    {"breed_id": "001", "synset_id": "n02085620", "class_idx": 0,  "name_en": "Chihuahua",                      "name_zh": "吉娃娃"},
    {"breed_id": "002", "synset_id": "n02085782", "class_idx": 1,  "name_en": "Japanese_spaniel",               "name_zh": "日本狆"},
    {"breed_id": "003", "synset_id": "n02085936", "class_idx": 2,  "name_en": "Maltese_dog",                    "name_zh": "马尔济斯犬"},
    {"breed_id": "004", "synset_id": "n02086079", "class_idx": 3,  "name_en": "Pekinese",                       "name_zh": "北京犬"},
    {"breed_id": "005", "synset_id": "n02086240", "class_idx": 4,  "name_en": "Shih-Tzu",                       "name_zh": "西施犬"},
    {"breed_id": "006", "synset_id": "n02086646", "class_idx": 5,  "name_en": "Blenheim_spaniel",               "name_zh": "骑士查理王小猎犬"},
    {"breed_id": "007", "synset_id": "n02086910", "class_idx": 6,  "name_en": "papillon",                       "name_zh": "蝴蝶犬"},
    {"breed_id": "008", "synset_id": "n02087046", "class_idx": 7,  "name_en": "toy_terrier",                    "name_zh": "玩具梗犬"},
    {"breed_id": "009", "synset_id": "n02087394", "class_idx": 8,  "name_en": "Rhodesian_ridgeback",            "name_zh": "罗德西亚脊背犬"},
    {"breed_id": "010", "synset_id": "n02088094", "class_idx": 9,  "name_en": "Afghan_hound",                   "name_zh": "阿富汗猎犬"},
    {"breed_id": "011", "synset_id": "n02088238", "class_idx": 10, "name_en": "basset",                         "name_zh": "巴吉度猎犬"},
    {"breed_id": "012", "synset_id": "n02088364", "class_idx": 11, "name_en": "beagle",                         "name_zh": "比格犬"},
    {"breed_id": "013", "synset_id": "n02088466", "class_idx": 12, "name_en": "bloodhound",                     "name_zh": "寻血猎犬"},
    {"breed_id": "014", "synset_id": "n02088632", "class_idx": 13, "name_en": "bluetick",                       "name_zh": "蓝斑猎浣熊犬"},
    {"breed_id": "015", "synset_id": "n02089078", "class_idx": 14, "name_en": "black-and-tan_coonhound",        "name_zh": "黑棕猎浣熊犬"},
    {"breed_id": "016", "synset_id": "n02089867", "class_idx": 15, "name_en": "Walker_hound",                   "name_zh": "步行猎犬"},
    {"breed_id": "017", "synset_id": "n02089973", "class_idx": 16, "name_en": "English_foxhound",               "name_zh": "英国猎狐犬"},
    {"breed_id": "018", "synset_id": "n02090379", "class_idx": 17, "name_en": "redbone",                        "name_zh": "红骨猎浣熊犬"},
    {"breed_id": "019", "synset_id": "n02090622", "class_idx": 18, "name_en": "borzoi",                         "name_zh": "苏俄猎狼犬"},
    {"breed_id": "020", "synset_id": "n02090721", "class_idx": 19, "name_en": "Irish_wolfhound",                "name_zh": "爱尔兰猎狼犬"},
    {"breed_id": "021", "synset_id": "n02091032", "class_idx": 20, "name_en": "Italian_greyhound",              "name_zh": "意大利灵缇"},
    {"breed_id": "022", "synset_id": "n02091134", "class_idx": 21, "name_en": "whippet",                        "name_zh": "惠比特犬"},
    {"breed_id": "023", "synset_id": "n02091244", "class_idx": 22, "name_en": "Ibizan_hound",                   "name_zh": "伊比赞猎犬"},
    {"breed_id": "024", "synset_id": "n02091467", "class_idx": 23, "name_en": "Norwegian_elkhound",             "name_zh": "挪威猎麋犬"},
    {"breed_id": "025", "synset_id": "n02091635", "class_idx": 24, "name_en": "otterhound",                     "name_zh": "水獭猎犬"},
    {"breed_id": "026", "synset_id": "n02091831", "class_idx": 25, "name_en": "Saluki",                         "name_zh": "萨路基猎犬"},
    {"breed_id": "027", "synset_id": "n02092002", "class_idx": 26, "name_en": "Scottish_deerhound",             "name_zh": "苏格兰猎鹿犬"},
    {"breed_id": "028", "synset_id": "n02092339", "class_idx": 27, "name_en": "Weimaraner",                     "name_zh": "威玛猎犬"},
    {"breed_id": "029", "synset_id": "n02093256", "class_idx": 28, "name_en": "Staffordshire_bullterrier",      "name_zh": "斯塔福郡斗牛梗"},
    {"breed_id": "030", "synset_id": "n02093428", "class_idx": 29, "name_en": "American_Staffordshire_terrier", "name_zh": "美国斯塔福郡梗"},
    {"breed_id": "031", "synset_id": "n02093647", "class_idx": 30, "name_en": "Bedlington_terrier",             "name_zh": "贝灵顿梗"},
    {"breed_id": "032", "synset_id": "n02093754", "class_idx": 31, "name_en": "Border_terrier",                 "name_zh": "边境梗"},
    {"breed_id": "033", "synset_id": "n02093859", "class_idx": 32, "name_en": "Kerry_blue_terrier",             "name_zh": "凯利蓝梗"},
    {"breed_id": "034", "synset_id": "n02093991", "class_idx": 33, "name_en": "Irish_terrier",                  "name_zh": "爱尔兰梗"},
    {"breed_id": "035", "synset_id": "n02094114", "class_idx": 34, "name_en": "Norfolk_terrier",                "name_zh": "诺福克梗"},
    {"breed_id": "036", "synset_id": "n02094258", "class_idx": 35, "name_en": "Norwich_terrier",                "name_zh": "诺里奇梗"},
    {"breed_id": "037", "synset_id": "n02094433", "class_idx": 36, "name_en": "Yorkshire_terrier",              "name_zh": "约克夏梗"},
    {"breed_id": "038", "synset_id": "n02095314", "class_idx": 37, "name_en": "wire-haired_fox_terrier",        "name_zh": "刚毛猎狐梗"},
    {"breed_id": "039", "synset_id": "n02095570", "class_idx": 38, "name_en": "Lakeland_terrier",               "name_zh": "湖畔梗"},
    {"breed_id": "040", "synset_id": "n02095889", "class_idx": 39, "name_en": "Sealyham_terrier",               "name_zh": "西里汉梗"},
    {"breed_id": "041", "synset_id": "n02096051", "class_idx": 40, "name_en": "Airedale",                       "name_zh": "万能梗"},
    {"breed_id": "042", "synset_id": "n02096177", "class_idx": 41, "name_en": "cairn",                          "name_zh": "凯恩梗"},
    {"breed_id": "043", "synset_id": "n02096294", "class_idx": 42, "name_en": "Australian_terrier",             "name_zh": "澳大利亚梗"},
    {"breed_id": "044", "synset_id": "n02096437", "class_idx": 43, "name_en": "Dandie_Dinmont",                 "name_zh": "丹迪丁蒙梗"},
    {"breed_id": "045", "synset_id": "n02096585", "class_idx": 44, "name_en": "Boston_bull",                    "name_zh": "波士顿梗"},
    {"breed_id": "046", "synset_id": "n02097047", "class_idx": 45, "name_en": "miniature_schnauzer",            "name_zh": "迷你雪纳瑞"},
    {"breed_id": "047", "synset_id": "n02097130", "class_idx": 46, "name_en": "giant_schnauzer",                "name_zh": "巨型雪纳瑞"},
    {"breed_id": "048", "synset_id": "n02097209", "class_idx": 47, "name_en": "standard_schnauzer",             "name_zh": "标准雪纳瑞"},
    {"breed_id": "049", "synset_id": "n02097298", "class_idx": 48, "name_en": "Scotch_terrier",                 "name_zh": "苏格兰梗"},
    {"breed_id": "050", "synset_id": "n02097474", "class_idx": 49, "name_en": "Tibetan_terrier",                "name_zh": "西藏梗"},
    {"breed_id": "051", "synset_id": "n02097658", "class_idx": 50, "name_en": "silky_terrier",                  "name_zh": "丝毛梗"},
    {"breed_id": "052", "synset_id": "n02098105", "class_idx": 51, "name_en": "soft-coated_wheaten_terrier",    "name_zh": "软毛麦色梗"},
    {"breed_id": "053", "synset_id": "n02098286", "class_idx": 52, "name_en": "West_Highland_white_terrier",    "name_zh": "西高地白梗"},
    {"breed_id": "054", "synset_id": "n02098413", "class_idx": 53, "name_en": "Lhasa",                          "name_zh": "拉萨犬"},
    {"breed_id": "055", "synset_id": "n02099267", "class_idx": 54, "name_en": "flat-coated_retriever",          "name_zh": "平毛寻回犬"},
    {"breed_id": "056", "synset_id": "n02099429", "class_idx": 55, "name_en": "curly-coated_retriever",         "name_zh": "卷毛寻回犬"},
    {"breed_id": "057", "synset_id": "n02099601", "class_idx": 56, "name_en": "golden_retriever",               "name_zh": "金毛寻回犬"},
    {"breed_id": "058", "synset_id": "n02099712", "class_idx": 57, "name_en": "Labrador_retriever",             "name_zh": "拉布拉多寻回犬"},
    {"breed_id": "059", "synset_id": "n02099849", "class_idx": 58, "name_en": "Chesapeake_Bay_retriever",       "name_zh": "切萨皮克湾寻回犬"},
    {"breed_id": "060", "synset_id": "n02100236", "class_idx": 59, "name_en": "German_short-haired_pointer",    "name_zh": "德国短毛指示犬"},
    {"breed_id": "061", "synset_id": "n02100583", "class_idx": 60, "name_en": "vizsla",                         "name_zh": "匈牙利维兹拉犬"},
    {"breed_id": "062", "synset_id": "n02100735", "class_idx": 61, "name_en": "English_setter",                 "name_zh": "英国雪达犬"},
    {"breed_id": "063", "synset_id": "n02100877", "class_idx": 62, "name_en": "Irish_setter",                   "name_zh": "爱尔兰雪达犬"},
    {"breed_id": "064", "synset_id": "n02101006", "class_idx": 63, "name_en": "Gordon_setter",                  "name_zh": "戈登雪达犬"},
    {"breed_id": "065", "synset_id": "n02101388", "class_idx": 64, "name_en": "Brittany_spaniel",               "name_zh": "布列塔尼犬"},
    {"breed_id": "066", "synset_id": "n02101556", "class_idx": 65, "name_en": "clumber",                        "name_zh": "克伦伯猎鹬犬"},
    {"breed_id": "067", "synset_id": "n02102040", "class_idx": 66, "name_en": "English_springer",               "name_zh": "英国激飞猎犬"},
    {"breed_id": "068", "synset_id": "n02102177", "class_idx": 67, "name_en": "Welsh_springer_spaniel",         "name_zh": "威尔士激飞猎犬"},
    {"breed_id": "069", "synset_id": "n02102318", "class_idx": 68, "name_en": "cocker_spaniel",                 "name_zh": "可卡犬"},
    {"breed_id": "070", "synset_id": "n02102480", "class_idx": 69, "name_en": "Sussex_spaniel",                 "name_zh": "萨塞克斯猎犬"},
    {"breed_id": "071", "synset_id": "n02102973", "class_idx": 70, "name_en": "Irish_water_spaniel",            "name_zh": "爱尔兰水猎犬"},
    {"breed_id": "072", "synset_id": "n02104029", "class_idx": 71, "name_en": "kuvasz",                         "name_zh": "库瓦兹犬"},
    {"breed_id": "073", "synset_id": "n02104365", "class_idx": 72, "name_en": "schipperke",                     "name_zh": "史奇派克犬"},
    {"breed_id": "074", "synset_id": "n02105056", "class_idx": 73, "name_en": "groenendael",                    "name_zh": "格罗安达犬"},
    {"breed_id": "075", "synset_id": "n02105162", "class_idx": 74, "name_en": "malinois",                       "name_zh": "比利时马林诺斯犬"},
    {"breed_id": "076", "synset_id": "n02105251", "class_idx": 75, "name_en": "briard",                         "name_zh": "伯瑞犬"},
    {"breed_id": "077", "synset_id": "n02105412", "class_idx": 76, "name_en": "kelpie",                         "name_zh": "澳大利亚凯尔皮犬"},
    {"breed_id": "078", "synset_id": "n02105505", "class_idx": 77, "name_en": "komondor",                       "name_zh": "可蒙犬"},
    {"breed_id": "079", "synset_id": "n02105641", "class_idx": 78, "name_en": "Old_English_sheepdog",           "name_zh": "英国古代牧羊犬"},
    {"breed_id": "080", "synset_id": "n02105855", "class_idx": 79, "name_en": "Shetland_sheepdog",              "name_zh": "喜乐蒂牧羊犬"},
    {"breed_id": "081", "synset_id": "n02106030", "class_idx": 80, "name_en": "collie",                         "name_zh": "柯利牧羊犬"},
    {"breed_id": "082", "synset_id": "n02106166", "class_idx": 81, "name_en": "Border_collie",                  "name_zh": "边境牧羊犬"},
    {"breed_id": "083", "synset_id": "n02106382", "class_idx": 82, "name_en": "Bouvier_des_Flandres",           "name_zh": "法兰德斯牧牛犬"},
    {"breed_id": "084", "synset_id": "n02106550", "class_idx": 83, "name_en": "Rottweiler",                     "name_zh": "罗威纳犬"},
    {"breed_id": "085", "synset_id": "n02106662", "class_idx": 84, "name_en": "German_shepherd",                "name_zh": "德国牧羊犬"},
    {"breed_id": "086", "synset_id": "n02107142", "class_idx": 85, "name_en": "Doberman",                       "name_zh": "杜宾犬"},
    {"breed_id": "087", "synset_id": "n02107312", "class_idx": 86, "name_en": "miniature_pinscher",             "name_zh": "迷你杜宾犬"},
    {"breed_id": "088", "synset_id": "n02107574", "class_idx": 87, "name_en": "Greater_Swiss_Mountain_dog",     "name_zh": "大瑞士山地犬"},
    {"breed_id": "089", "synset_id": "n02107683", "class_idx": 88, "name_en": "Bernese_mountain_dog",           "name_zh": "伯恩山犬"},
    {"breed_id": "090", "synset_id": "n02107908", "class_idx": 89, "name_en": "Appenzeller",                    "name_zh": "阿彭策尔山犬"},
    {"breed_id": "091", "synset_id": "n02108000", "class_idx": 90, "name_en": "EntleBucher",                    "name_zh": "恩特雷布赫山地犬"},
    {"breed_id": "092", "synset_id": "n02108089", "class_idx": 91, "name_en": "boxer",                          "name_zh": "拳师犬"},
    {"breed_id": "093", "synset_id": "n02108422", "class_idx": 92, "name_en": "bull_mastiff",                   "name_zh": "斗牛獒犬"},
    {"breed_id": "094", "synset_id": "n02108551", "class_idx": 93, "name_en": "Tibetan_mastiff",                "name_zh": "藏獒"},
    {"breed_id": "095", "synset_id": "n02108915", "class_idx": 94, "name_en": "French_bulldog",                 "name_zh": "法国斗牛犬"},
    {"breed_id": "096", "synset_id": "n02109047", "class_idx": 95, "name_en": "Great_Dane",                     "name_zh": "大丹犬"},
    {"breed_id": "097", "synset_id": "n02109525", "class_idx": 96, "name_en": "Saint_Bernard",                  "name_zh": "圣伯纳犬"},
    {"breed_id": "098", "synset_id": "n02109961", "class_idx": 97, "name_en": "Eskimo_dog",                     "name_zh": "爱斯基摩犬"},
    {"breed_id": "099", "synset_id": "n02110063", "class_idx": 98, "name_en": "malamute",                       "name_zh": "阿拉斯加雪橇犬"},
    {"breed_id": "100", "synset_id": "n02110185", "class_idx": 99, "name_en": "Siberian_husky",                 "name_zh": "西伯利亚雪橇犬"},
    {"breed_id": "101", "synset_id": "n02110627", "class_idx": 100,"name_en": "affenpinscher",                  "name_zh": "猴面犬"},
    {"breed_id": "102", "synset_id": "n02110806", "class_idx": 101,"name_en": "basenji",                        "name_zh": "巴辛吉犬"},
    {"breed_id": "103", "synset_id": "n02110958", "class_idx": 102,"name_en": "pug",                            "name_zh": "巴哥犬"},
    {"breed_id": "104", "synset_id": "n02111129", "class_idx": 103,"name_en": "Leonberg",                       "name_zh": "莱昂贝格犬"},
    {"breed_id": "105", "synset_id": "n02111277", "class_idx": 104,"name_en": "Newfoundland",                   "name_zh": "纽芬兰犬"},
    {"breed_id": "106", "synset_id": "n02111500", "class_idx": 105,"name_en": "Great_Pyrenees",                 "name_zh": "大白熊犬"},
    {"breed_id": "107", "synset_id": "n02111889", "class_idx": 106,"name_en": "Samoyed",                        "name_zh": "萨摩耶犬"},
    {"breed_id": "108", "synset_id": "n02112018", "class_idx": 107,"name_en": "Pomeranian",                     "name_zh": "博美犬"},
    {"breed_id": "109", "synset_id": "n02112137", "class_idx": 108,"name_en": "chow",                           "name_zh": "松狮犬"},
    {"breed_id": "110", "synset_id": "n02112350", "class_idx": 109,"name_en": "keeshond",                       "name_zh": "荷兰毛狮犬"},
    {"breed_id": "111", "synset_id": "n02112706", "class_idx": 110,"name_en": "Brabancon_griffon",              "name_zh": "布鲁塞尔格里芬犬"},
    {"breed_id": "112", "synset_id": "n02113023", "class_idx": 111,"name_en": "Pembroke",                       "name_zh": "彭布罗克威尔士柯基犬"},
    {"breed_id": "113", "synset_id": "n02113186", "class_idx": 112,"name_en": "Cardigan",                       "name_zh": "卡迪根威尔士柯基犬"},
    {"breed_id": "114", "synset_id": "n02113624", "class_idx": 113,"name_en": "toy_poodle",                     "name_zh": "玩具贵宾犬"},
    {"breed_id": "115", "synset_id": "n02113712", "class_idx": 114,"name_en": "miniature_poodle",               "name_zh": "迷你贵宾犬"},
    {"breed_id": "116", "synset_id": "n02113799", "class_idx": 115,"name_en": "standard_poodle",                "name_zh": "标准贵宾犬"},
    {"breed_id": "117", "synset_id": "n02113978", "class_idx": 116,"name_en": "Mexican_hairless",               "name_zh": "墨西哥无毛犬"},
    {"breed_id": "118", "synset_id": "n02115641", "class_idx": 117,"name_en": "dingo",                          "name_zh": "澳洲野犬"},
    {"breed_id": "119", "synset_id": "n02115913", "class_idx": 118,"name_en": "dhole",                          "name_zh": "豺犬"},
    {"breed_id": "120", "synset_id": "n02116738", "class_idx": 119,"name_en": "African_hunting_dog",            "name_zh": "非洲猎犬"},
]

# 快速查找索引
SYNSET_TO_BREED: dict[str, dict] = {b["synset_id"]: b for b in BREED_MAP}
CLASS_TO_BREED: dict[int, dict] = {b["class_idx"]: b for b in BREED_MAP}
BREED_ID_TO_BREED: dict[str, dict] = {b["breed_id"]: b for b in BREED_MAP}
NAME_EN_TO_BREED: dict[str, dict] = {b["name_en"].lower(): b for b in BREED_MAP}
NAME_ZH_TO_BREED: dict[str, dict] = {b["name_zh"]: b for b in BREED_MAP}
SYNSET_TO_CLASS: dict[str, int] = {b["synset_id"]: b["class_idx"] for b in BREED_MAP}
CLASS_TO_SYNSET: dict[int, str] = {b["class_idx"]: b["synset_id"] for b in BREED_MAP}
BREED_ID_TO_CLASS: dict[str, int] = {b["breed_id"]: b["class_idx"] for b in BREED_MAP}
CLASS_TO_BREED_ID: dict[int, str] = {b["class_idx"]: b["breed_id"] for b in BREED_MAP}

NUM_CLASSES: int = len(BREED_MAP)  # 120

# ====== main.py 兼容别名 ======
STANFORD_BREED_MAP = BREED_MAP
SORTED_SYNSETS = sorted(SYNSET_TO_BREED.keys())


def get_class_names() -> list:
    """
    返回 120 个品种中文名, 按 class_idx 顺序排列
    用于 main.py 启动时传给推理引擎
    """
    return [b["name_zh"] for b in sorted(BREED_MAP, key=lambda x: x["class_idx"])]


def build_id_to_breedid_map() -> dict:
    """
    返回 class_idx (字符串) → breed_id 的映射
    例如: {"0": "001", "1": "002", ..., "119": "120"}
    用于 main.py 启动时索引回 breed_id
    """
    return {str(b["class_idx"]): b["breed_id"] for b in BREED_MAP}


# ====== 跨数据集桥接: breed_mapping name_en → breeds_data breed_id ======

import sys
from pathlib import Path

# 延迟导入 breeds_data 以避免循环依赖
_BREED_DATA_INDEX_BY_NAME = None


def _get_breed_data_index():
    """延迟加载 breeds_data 的 name_en 索引"""
    global _BREED_DATA_INDEX_BY_NAME
    if _BREED_DATA_INDEX_BY_NAME is None:
        try:
            _backend_dir = str(Path(__file__).resolve().parent.parent)
            if _backend_dir not in sys.path:
                sys.path.insert(0, _backend_dir)
            from breeds_data import BREEDS_DATA
            # 为每个品种建立多个格式的索引，以支持不同来源的 name_en 匹配
            _BREED_DATA_INDEX_BY_NAME = {}
            for b in BREEDS_DATA:
                # 格式1: 原始格式（通常是 "Siberian Husky" 空格分隔）
                key1 = b["name_en"].lower().strip()
                _BREED_DATA_INDEX_BY_NAME[key1] = b
                # 格式2: 下划线格式（breed_mapping.py 格式："siberian_husky"）
                key2 = key1.replace(' ', '_')
                if key2 not in _BREED_DATA_INDEX_BY_NAME:
                    _BREED_DATA_INDEX_BY_NAME[key2] = b
                # 格式3: 无空格格式（"siberianhusky"）
                key3 = key1.replace(' ', '')
                if key3 not in _BREED_DATA_INDEX_BY_NAME:
                    _BREED_DATA_INDEX_BY_NAME[key3] = b
        except ImportError:
            _BREED_DATA_INDEX_BY_NAME = {}
    return _BREED_DATA_INDEX_BY_NAME


def normalize_breed_name(name: str) -> str:
    """标准化品种名: 小写, 统一分隔符为空格"""
    return name.lower().replace('_', ' ').replace('-', ' ').strip()


def find_data_breed_id(mapping_name_en: str) -> str:
    """
    通过英文名匹配, 返回 breeds_data.py 中对应的 breed_id

    如果找不到匹配, 返回原始的 mapping breed_id (通过 name_en 在 BREED_MAP 中反查)
    """
    data_index = _get_breed_data_index()
    if not data_index:
        return None

    key = normalize_breed_name(mapping_name_en)

    # 精确匹配（多种格式）
    match = data_index.get(key)
    if match:
        return match["breed_id"]

    # 也尝试下划线版本
    key_underscore = key.replace(' ', '_')
    match = data_index.get(key_underscore)
    if match:
        return match["breed_id"]

    # 模糊匹配: 子串/包含关系
    for dk, dv in data_index.items():
        if key in dk or dk in key:
            if len(key) >= 5 and len(dk) >= 5:
                return dv["breed_id"]

    # 去除 "dog" 后缀后再试
    key_no_dog = key.replace(' dog', '')
    if key_no_dog != key:
        for dk, dv in data_index.items():
            dk_no_dog = dk.replace(' dog', '')
            if key_no_dog == dk_no_dog:
                return dv["breed_id"]

    return None


def find_data_breed_by_name_en(mapping_name_en: str) -> dict:
    """
    通过英文名匹配, 返回 breeds_data.py 中的完整品种字典
    """
    data_index = _get_breed_data_index()
    if not data_index:
        return None

    key = normalize_breed_name(mapping_name_en)

    # 精确匹配（多种格式）
    match = data_index.get(key)
    if match:
        return match

    key_underscore = key.replace(' ', '_')
    match = data_index.get(key_underscore)
    if match:
        return match

    # 模糊匹配
    for dk, dv in data_index.items():
        if key in dk or dk in key:
            if len(key) >= 5 and len(dk) >= 5:
                return dv

    key_no_dog = key.replace(' dog', '')
    if key_no_dog != key:
        for dk, dv in data_index.items():
            if dk.replace(' dog', '') == key_no_dog:
                return dv

    return None
