"""
Kaggle Notebook 训练脚本 — 犬博士 (dog-doctor)
==============================================
使用方法：将本文件上传到 Kaggle Notebook，添加 Stanford Dogs Dataset，
然后在 Notebook 中运行：!python kaggle_train.py
"""

import os, json, time, logging
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import ReduceLROnPlateau, CosineAnnealingLR
from torch.utils.data import DataLoader, Dataset, random_split
from torchvision import transforms, models
from PIL import Image
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# ============================================================
# 配置参数
# ============================================================

# 路径：自动搜索 Stanford Dogs 图片目录（不依赖固定数据集名称）
KAGGLE_DATA_DIR = Path("/kaggle/input")
RAW_IMAGE_DIR = None

# 先尝试常见路径（包括 datasets/用户名 子目录）
for candidate in [
    KAGGLE_DATA_DIR / "datasets" / "jessicali9530" / "stanford-dogs-dataset" / "images" / "Images",
    KAGGLE_DATA_DIR / "datasets" / "jessicali9530" / "images" / "Images",
    KAGGLE_DATA_DIR / "datasets" / "jessicali9530" / "stanford-dogs-dataset" / "Images",
    KAGGLE_DATA_DIR / "datasets" / "jessicali9530" / "Images",
    KAGGLE_DATA_DIR / "datasets" / "images" / "Images",
    KAGGLE_DATA_DIR / "datasets" / "Images",
    KAGGLE_DATA_DIR / "stanford-dogs-dataset" / "images" / "Images",
    KAGGLE_DATA_DIR / "stanford-dogs-dataset" / "Images",
    KAGGLE_DATA_DIR / "images" / "Images",
]:
    if candidate.exists() and any(candidate.iterdir()):
        RAW_IMAGE_DIR = candidate
        break

# 兜底：遍历 /kaggle/input 下所有目录，搜索包含 n020* 品种文件夹的目录
if not RAW_IMAGE_DIR:
    for p in KAGGLE_DATA_DIR.rglob("*"):
        if p.is_dir() and "n02085620" in [d.name for d in p.iterdir()]:
            RAW_IMAGE_DIR = p
            break

if not RAW_IMAGE_DIR:
    raise FileNotFoundError(
        f"找不到 Stanford Dogs 图片目录！请确认已在右侧 Data 面板中添加数据集。\n"
        f"已搜索: {KAGGLE_DATA_DIR}"
    )

logger.info(f"图片目录: {RAW_IMAGE_DIR}")

OUTPUT_DIR = Path("/kaggle/working/dog_doctor_output")
MODEL_DIR = OUTPUT_DIR / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# 训练参数
IMAGE_SIZE, RESIZE_SIZE = 224, 256
BATCH_SIZE, NUM_WORKERS = 32, 2
LEARNING_RATE, FINE_TUNE_LR, WEIGHT_DECAY = 0.001, 0.0001, 1e-4
STAGE1_EPOCHS, STAGE2_EPOCHS, STAGE3_EPOCHS = 5, 15, 30
TRAIN_RATIO, VAL_RATIO = 0.70, 0.15
MEAN, STD = [0.485, 0.456, 0.406], [0.229, 0.224, 0.225]

# 设备
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logger.info(f"设备: {DEVICE}")
if DEVICE.type == "cpu":
    logger.warning("⚠️ 使用 CPU 训练！请在 Settings → Accelerator 中开启 GPU")

# ============================================================
# 犬种映射表 (120类)
# ============================================================

BREED_MAP = [
    {"breed_id": "001", "synset_id": "n02085620", "name_en": "Chihuahua", "name_zh": "吉娃娃"},
    {"breed_id": "002", "synset_id": "n02085782", "name_en": "Japanese_spaniel", "name_zh": "日本狆"},
    {"breed_id": "003", "synset_id": "n02085936", "name_en": "Maltese_dog", "name_zh": "马尔济斯犬"},
    {"breed_id": "004", "synset_id": "n02086079", "name_en": "Pekinese", "name_zh": "北京犬"},
    {"breed_id": "005", "synset_id": "n02086240", "name_en": "Shih-Tzu", "name_zh": "西施犬"},
    {"breed_id": "006", "synset_id": "n02086646", "name_en": "Blenheim_spaniel", "name_zh": "骑士查理王小猎犬"},
    {"breed_id": "007", "synset_id": "n02086910", "name_en": "papillon", "name_zh": "蝴蝶犬"},
    {"breed_id": "008", "synset_id": "n02087046", "name_en": "toy_terrier", "name_zh": "玩具梗犬"},
    {"breed_id": "009", "synset_id": "n02087394", "name_en": "Rhodesian_ridgeback", "name_zh": "罗德西亚脊背犬"},
    {"breed_id": "010", "synset_id": "n02088094", "name_en": "Afghan_hound", "name_zh": "阿富汗猎犬"},
    {"breed_id": "011", "synset_id": "n02088238", "name_en": "basset", "name_zh": "巴吉度猎犬"},
    {"breed_id": "012", "synset_id": "n02088364", "name_en": "beagle", "name_zh": "比格犬"},
    {"breed_id": "013", "synset_id": "n02088466", "name_en": "bloodhound", "name_zh": "寻血猎犬"},
    {"breed_id": "014", "synset_id": "n02088632", "name_en": "bluetick", "name_zh": "蓝斑猎浣熊犬"},
    {"breed_id": "015", "synset_id": "n02089078", "name_en": "black-and-tan_coonhound", "name_zh": "黑棕猎浣熊犬"},
    {"breed_id": "016", "synset_id": "n02089867", "name_en": "Walker_hound", "name_zh": "步行猎犬"},
    {"breed_id": "017", "synset_id": "n02089973", "name_en": "English_foxhound", "name_zh": "英国猎狐犬"},
    {"breed_id": "018", "synset_id": "n02090379", "name_en": "redbone", "name_zh": "红骨猎浣熊犬"},
    {"breed_id": "019", "synset_id": "n02090622", "name_en": "borzoi", "name_zh": "苏俄猎狼犬"},
    {"breed_id": "020", "synset_id": "n02090721", "name_en": "Irish_wolfhound", "name_zh": "爱尔兰猎狼犬"},
    {"breed_id": "021", "synset_id": "n02091032", "name_en": "Italian_greyhound", "name_zh": "意大利灵缇"},
    {"breed_id": "022", "synset_id": "n02091134", "name_en": "whippet", "name_zh": "惠比特犬"},
    {"breed_id": "023", "synset_id": "n02091244", "name_en": "Ibizan_hound", "name_zh": "伊比赞猎犬"},
    {"breed_id": "024", "synset_id": "n02091467", "name_en": "Norwegian_elkhound", "name_zh": "挪威猎麋犬"},
    {"breed_id": "025", "synset_id": "n02091635", "name_en": "otterhound", "name_zh": "水獭猎犬"},
    {"breed_id": "026", "synset_id": "n02091831", "name_en": "Saluki", "name_zh": "萨路基猎犬"},
    {"breed_id": "027", "synset_id": "n02092002", "name_en": "Scottish_deerhound", "name_zh": "苏格兰猎鹿犬"},
    {"breed_id": "028", "synset_id": "n02092339", "name_en": "Weimaraner", "name_zh": "威玛猎犬"},
    {"breed_id": "029", "synset_id": "n02093256", "name_en": "Staffordshire_bullterrier", "name_zh": "斯塔福郡斗牛梗"},
    {"breed_id": "030", "synset_id": "n02093428", "name_en": "American_Staffordshire_terrier", "name_zh": "美国斯塔福郡梗"},
    {"breed_id": "031", "synset_id": "n02093647", "name_en": "Bedlington_terrier", "name_zh": "贝灵顿梗"},
    {"breed_id": "032", "synset_id": "n02093754", "name_en": "Border_terrier", "name_zh": "边境梗"},
    {"breed_id": "033", "synset_id": "n02093859", "name_en": "Kerry_blue_terrier", "name_zh": "凯利蓝梗"},
    {"breed_id": "034", "synset_id": "n02093991", "name_en": "Irish_terrier", "name_zh": "爱尔兰梗"},
    {"breed_id": "035", "synset_id": "n02094114", "name_en": "Norfolk_terrier", "name_zh": "诺福克梗"},
    {"breed_id": "036", "synset_id": "n02094258", "name_en": "Norwich_terrier", "name_zh": "诺里奇梗"},
    {"breed_id": "037", "synset_id": "n02094433", "name_en": "Yorkshire_terrier", "name_zh": "约克夏梗"},
    {"breed_id": "038", "synset_id": "n02095314", "name_en": "wire-haired_fox_terrier", "name_zh": "刚毛猎狐梗"},
    {"breed_id": "039", "synset_id": "n02095570", "name_en": "Lakeland_terrier", "name_zh": "湖畔梗"},
    {"breed_id": "040", "synset_id": "n02095889", "name_en": "Sealyham_terrier", "name_zh": "西里汉梗"},
    {"breed_id": "041", "synset_id": "n02096051", "name_en": "Airedale", "name_zh": "万能梗"},
    {"breed_id": "042", "synset_id": "n02096177", "name_en": "cairn", "name_zh": "凯恩梗"},
    {"breed_id": "043", "synset_id": "n02096294", "name_en": "Australian_terrier", "name_zh": "澳大利亚梗"},
    {"breed_id": "044", "synset_id": "n02096437", "name_en": "Dandie_Dinmont", "name_zh": "丹迪丁蒙梗"},
    {"breed_id": "045", "synset_id": "n02096585", "name_en": "Boston_bull", "name_zh": "波士顿梗"},
    {"breed_id": "046", "synset_id": "n02097047", "name_en": "miniature_schnauzer", "name_zh": "迷你雪纳瑞"},
    {"breed_id": "047", "synset_id": "n02097130", "name_en": "giant_schnauzer", "name_zh": "巨型雪纳瑞"},
    {"breed_id": "048", "synset_id": "n02097209", "name_en": "standard_schnauzer", "name_zh": "标准雪纳瑞"},
    {"breed_id": "049", "synset_id": "n02097298", "name_en": "Scotch_terrier", "name_zh": "苏格兰梗"},
    {"breed_id": "050", "synset_id": "n02097474", "name_en": "Tibetan_terrier", "name_zh": "西藏梗"},
    {"breed_id": "051", "synset_id": "n02097658", "name_en": "silky_terrier", "name_zh": "丝毛梗"},
    {"breed_id": "052", "synset_id": "n02098105", "name_en": "soft-coated_wheaten_terrier", "name_zh": "软毛麦色梗"},
    {"breed_id": "053", "synset_id": "n02098286", "name_en": "West_Highland_white_terrier", "name_zh": "西高地白梗"},
    {"breed_id": "054", "synset_id": "n02098413", "name_en": "Lhasa", "name_zh": "拉萨犬"},
    {"breed_id": "055", "synset_id": "n02099267", "name_en": "flat-coated_retriever", "name_zh": "平毛寻回犬"},
    {"breed_id": "056", "synset_id": "n02099429", "name_en": "curly-coated_retriever", "name_zh": "卷毛寻回犬"},
    {"breed_id": "057", "synset_id": "n02099601", "name_en": "golden_retriever", "name_zh": "金毛寻回犬"},
    {"breed_id": "058", "synset_id": "n02099712", "name_en": "Labrador_retriever", "name_zh": "拉布拉多寻回犬"},
    {"breed_id": "059", "synset_id": "n02099849", "name_en": "Chesapeake_Bay_retriever", "name_zh": "切萨皮克湾寻回犬"},
    {"breed_id": "060", "synset_id": "n02100236", "name_en": "German_short-haired_pointer", "name_zh": "德国短毛指示犬"},
    {"breed_id": "061", "synset_id": "n02100583", "name_en": "vizsla", "name_zh": "匈牙利维兹拉犬"},
    {"breed_id": "062", "synset_id": "n02100735", "name_en": "English_setter", "name_zh": "英国雪达犬"},
    {"breed_id": "063", "synset_id": "n02100877", "name_en": "Irish_setter", "name_zh": "爱尔兰雪达犬"},
    {"breed_id": "064", "synset_id": "n02101006", "name_en": "Gordon_setter", "name_zh": "戈登雪达犬"},
    {"breed_id": "065", "synset_id": "n02101388", "name_en": "Brittany_spaniel", "name_zh": "布列塔尼犬"},
    {"breed_id": "066", "synset_id": "n02101556", "name_en": "clumber", "name_zh": "克伦伯猎鹬犬"},
    {"breed_id": "067", "synset_id": "n02102040", "name_en": "English_springer", "name_zh": "英国激飞猎犬"},
    {"breed_id": "068", "synset_id": "n02102177", "name_en": "Welsh_springer_spaniel", "name_zh": "威尔士激飞猎犬"},
    {"breed_id": "069", "synset_id": "n02102318", "name_en": "cocker_spaniel", "name_zh": "可卡犬"},
    {"breed_id": "070", "synset_id": "n02102480", "name_en": "Sussex_spaniel", "name_zh": "萨塞克斯猎犬"},
    {"breed_id": "071", "synset_id": "n02102973", "name_en": "Irish_water_spaniel", "name_zh": "爱尔兰水猎犬"},
    {"breed_id": "072", "synset_id": "n02104029", "name_en": "kuvasz", "name_zh": "库瓦兹犬"},
    {"breed_id": "073", "synset_id": "n02104365", "name_en": "schipperke", "name_zh": "史奇派克犬"},
    {"breed_id": "074", "synset_id": "n02105056", "name_en": "groenendael", "name_zh": "格罗安达犬"},
    {"breed_id": "075", "synset_id": "n02105162", "name_en": "malinois", "name_zh": "比利时马林诺斯犬"},
    {"breed_id": "076", "synset_id": "n02105251", "name_en": "briard", "name_zh": "伯瑞犬"},
    {"breed_id": "077", "synset_id": "n02105412", "name_en": "kelpie", "name_zh": "澳大利亚凯尔皮犬"},
    {"breed_id": "078", "synset_id": "n02105505", "name_en": "komondor", "name_zh": "可蒙犬"},
    {"breed_id": "079", "synset_id": "n02105641", "name_en": "Old_English_sheepdog", "name_zh": "英国古代牧羊犬"},
    {"breed_id": "080", "synset_id": "n02105855", "name_en": "Shetland_sheepdog", "name_zh": "喜乐蒂牧羊犬"},
    {"breed_id": "081", "synset_id": "n02106030", "name_en": "collie", "name_zh": "柯利牧羊犬"},
    {"breed_id": "082", "synset_id": "n02106166", "name_en": "Border_collie", "name_zh": "边境牧羊犬"},
    {"breed_id": "083", "synset_id": "n02106382", "name_en": "Bouvier_des_Flandres", "name_zh": "法兰德斯牧牛犬"},
    {"breed_id": "084", "synset_id": "n02106550", "name_en": "Rottweiler", "name_zh": "罗威纳犬"},
    {"breed_id": "085", "synset_id": "n02106662", "name_en": "German_shepherd", "name_zh": "德国牧羊犬"},
    {"breed_id": "086", "synset_id": "n02107142", "name_en": "Doberman", "name_zh": "杜宾犬"},
    {"breed_id": "087", "synset_id": "n02107312", "name_en": "miniature_pinscher", "name_zh": "迷你杜宾犬"},
    {"breed_id": "088", "synset_id": "n02107574", "name_en": "Greater_Swiss_Mountain_dog", "name_zh": "大瑞士山地犬"},
    {"breed_id": "089", "synset_id": "n02107683", "name_en": "Bernese_mountain_dog", "name_zh": "伯恩山犬"},
    {"breed_id": "090", "synset_id": "n02107908", "name_en": "Appenzeller", "name_zh": "阿彭策尔山犬"},
    {"breed_id": "091", "synset_id": "n02108000", "name_en": "EntleBucher", "name_zh": "恩特雷布赫山地犬"},
    {"breed_id": "092", "synset_id": "n02108089", "name_en": "boxer", "name_zh": "拳师犬"},
    {"breed_id": "093", "synset_id": "n02108422", "name_en": "bull_mastiff", "name_zh": "斗牛獒犬"},
    {"breed_id": "094", "synset_id": "n02108551", "name_en": "Tibetan_mastiff", "name_zh": "藏獒"},
    {"breed_id": "095", "synset_id": "n02108915", "name_en": "French_bulldog", "name_zh": "法国斗牛犬"},
    {"breed_id": "096", "synset_id": "n02109047", "name_en": "Great_Dane", "name_zh": "大丹犬"},
    {"breed_id": "097", "synset_id": "n02109525", "name_en": "Saint_Bernard", "name_zh": "圣伯纳犬"},
    {"breed_id": "098", "synset_id": "n02109961", "name_en": "Eskimo_dog", "name_zh": "爱斯基摩犬"},
    {"breed_id": "099", "synset_id": "n02110063", "name_en": "malamute", "name_zh": "阿拉斯加雪橇犬"},
    {"breed_id": "100", "synset_id": "n02110185", "name_en": "Siberian_husky", "name_zh": "西伯利亚雪橇犬"},
    {"breed_id": "101", "synset_id": "n02110627", "name_en": "affenpinscher", "name_zh": "猴面犬"},
    {"breed_id": "102", "synset_id": "n02110806", "name_en": "basenji", "name_zh": "巴辛吉犬"},
    {"breed_id": "103", "synset_id": "n02110958", "name_en": "pug", "name_zh": "巴哥犬"},
    {"breed_id": "104", "synset_id": "n02111129", "name_en": "Leonberg", "name_zh": "莱昂贝格犬"},
    {"breed_id": "105", "synset_id": "n02111277", "name_en": "Newfoundland", "name_zh": "纽芬兰犬"},
    {"breed_id": "106", "synset_id": "n02111500", "name_en": "Great_Pyrenees", "name_zh": "大白熊犬"},
    {"breed_id": "107", "synset_id": "n02111889", "name_en": "Samoyed", "name_zh": "萨摩耶犬"},
    {"breed_id": "108", "synset_id": "n02112018", "name_en": "Pomeranian", "name_zh": "博美犬"},
    {"breed_id": "109", "synset_id": "n02112137", "name_en": "chow", "name_zh": "松狮犬"},
    {"breed_id": "110", "synset_id": "n02112350", "name_en": "keeshond", "name_zh": "荷兰毛狮犬"},
    {"breed_id": "111", "synset_id": "n02112706", "name_en": "Brabancon_griffon", "name_zh": "布鲁塞尔格里芬犬"},
    {"breed_id": "112", "synset_id": "n02113023", "name_en": "Pembroke", "name_zh": "彭布罗克威尔士柯基犬"},
    {"breed_id": "113", "synset_id": "n02113186", "name_en": "Cardigan", "name_zh": "卡迪根威尔士柯基犬"},
    {"breed_id": "114", "synset_id": "n02113624", "name_en": "toy_poodle", "name_zh": "玩具贵宾犬"},
    {"breed_id": "115", "synset_id": "n02113712", "name_en": "miniature_poodle", "name_zh": "迷你贵宾犬"},
    {"breed_id": "116", "synset_id": "n02113799", "name_en": "standard_poodle", "name_zh": "标准贵宾犬"},
    {"breed_id": "117", "synset_id": "n02113978", "name_en": "Mexican_hairless", "name_zh": "墨西哥无毛犬"},
    {"breed_id": "118", "synset_id": "n02115641", "name_en": "dingo", "name_zh": "澳洲野犬"},
    {"breed_id": "119", "synset_id": "n02115913", "name_en": "dhole", "name_zh": "豺犬"},
    {"breed_id": "120", "synset_id": "n02116738", "name_en": "African_hunting_dog", "name_zh": "非洲猎犬"},
]

SYNSET_TO_CLASS = {b["synset_id"]: i for i, b in enumerate(BREED_MAP)}
NUM_CLASSES = len(BREED_MAP)
CLASS_NAMES_ZH = [b["name_zh"] for b in BREED_MAP]

# ============================================================
# 数据集
# ============================================================

class StanfordDogsDataset(Dataset):
    def __init__(self, root_dir, transform=None, mode="train", split_seed=42):
        self.root_dir = Path(root_dir)
        self.transform = transform
        self.mode = mode

        all_samples = []
        for breed_dir in sorted(self.root_dir.iterdir()):
            if not breed_dir.is_dir():
                continue
            synset_id = breed_dir.name.split("-")[0]
            if synset_id not in SYNSET_TO_CLASS:
                continue
            class_idx = SYNSET_TO_CLASS[synset_id]
            for img_file in breed_dir.glob("*.jpg"):
                all_samples.append((str(img_file), class_idx))

        if not all_samples:
            raise RuntimeError(f"在 {root_dir} 中未找到图片！")

        self._all_samples = all_samples

        if mode in ("train", "val", "test"):
            n = len(all_samples)
            n_train, n_val = int(n * TRAIN_RATIO), int(n * VAL_RATIO)
            n_test = n - n_train - n_val
            splits = random_split(all_samples, [n_train, n_val, n_test],
                                  generator=torch.Generator().manual_seed(split_seed))
            self.samples = splits[{"train": 0, "val": 1, "test": 2}[mode]]
        else:
            self.samples = all_samples

        logger.info(f"Dataset [{mode}]: {len(self.samples)} samples")

    def __len__(self): return len(self.samples)

    def __getitem__(self, idx):
        img_path, class_idx = self.samples[idx]
        image = Image.open(img_path).convert("RGB")
        return self.transform(image) if self.transform else image, class_idx


def get_train_transforms():
    return transforms.Compose([
        transforms.RandomResizedCrop(IMAGE_SIZE, scale=(0.8, 1.0)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
        transforms.ToTensor(),
        transforms.Normalize(mean=MEAN, std=STD),
    ])


def get_val_transforms():
    return transforms.Compose([
        transforms.Resize(RESIZE_SIZE),
        transforms.CenterCrop(IMAGE_SIZE),
        transforms.ToTensor(),
        transforms.Normalize(mean=MEAN, std=STD),
    ])


def create_dataloaders():
    train_ds = StanfordDogsDataset(RAW_IMAGE_DIR, get_train_transforms(), "train")
    val_ds = StanfordDogsDataset(RAW_IMAGE_DIR, get_val_transforms(), "val")
    test_ds = StanfordDogsDataset(RAW_IMAGE_DIR, get_val_transforms(), "test")
    return (
        DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True, num_workers=NUM_WORKERS, pin_memory=True),
        DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False, num_workers=NUM_WORKERS, pin_memory=True),
        DataLoader(test_ds, batch_size=BATCH_SIZE, shuffle=False, num_workers=NUM_WORKERS, pin_memory=True),
    )


# ============================================================
# 模型
# ============================================================

class DogBreedClassifier(nn.Module):
    def __init__(self, num_classes=NUM_CLASSES, dropout=0.5):
        super().__init__()
        self.backbone = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
        in_features = self.backbone.fc.in_features
        self.classifier = nn.Sequential(
            nn.Dropout(p=dropout),
            nn.Linear(in_features, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(inplace=True),
            nn.Dropout(p=dropout * 0.6),
            nn.Linear(512, num_classes),
        )
        self.backbone.fc = nn.Identity()
        nn.init.xavier_uniform_(self.classifier[5].weight)
        nn.init.zeros_(self.classifier[5].bias)

    def forward(self, x):
        return self.classifier(self.backbone(x))


def freeze_backbone(model, unfreeze_from=None):
    for name, param in model.named_parameters():
        if unfreeze_from and unfreeze_from in name:
            param.requires_grad = True
        elif "classifier" in name:
            param.requires_grad = True
        else:
            param.requires_grad = False
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total = sum(p.numel() for p in model.parameters())
    logger.info(f"可训练参数: {trainable:,} / {total:,} ({100*trainable/total:.1f}%)")


# ============================================================
# 训练 & 验证
# ============================================================

def train_one_epoch(model, loader, criterion, optimizer, epoch):
    model.train()
    running_loss, correct, total = 0.0, 0, 0
    scaler = torch.amp.GradScaler("cuda") if DEVICE.type == "cuda" else None

    for images, labels in tqdm(loader, desc=f"Epoch {epoch:3d} [Train]", leave=False):
        images, labels = images.to(DEVICE), labels.to(DEVICE)
        optimizer.zero_grad()

        if scaler:
            with torch.amp.autocast("cuda"):
                loss = criterion(model(images), labels)
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
        else:
            loss = criterion(model(images), labels)
            loss.backward()
            optimizer.step()

        running_loss += loss.item() * images.size(0)
        _, predicted = model(images).max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()

    return {"loss": running_loss / total, "accuracy": correct / total}


@torch.no_grad()
def validate(model, loader, criterion):
    model.eval()
    running_loss, correct_top1, correct_top5, total = 0.0, 0, 0, 0

    for images, labels in tqdm(loader, desc="Validate", leave=False):
        images, labels = images.to(DEVICE), labels.to(DEVICE)
        outputs = model(images)
        loss = criterion(outputs, labels)

        running_loss += loss.item() * images.size(0)
        total += labels.size(0)

        _, pred_top1 = outputs.max(1)
        correct_top1 += pred_top1.eq(labels).sum().item()

        _, pred_top5 = outputs.topk(5, dim=1)
        correct_top5 += pred_top5.eq(labels.view(-1, 1)).sum().item()

    return {
        "loss": running_loss / total,
        "top1_accuracy": correct_top1 / total,
        "top5_accuracy": correct_top5 / total,
    }


def save_checkpoint(model, path):
    torch.save({
        "model_state": model.state_dict(),
        "class_names": [f'{b["synset_id"]}-{b["name_en"]}' for b in BREED_MAP],
        "num_classes": NUM_CLASSES,
        "class_names_zh": CLASS_NAMES_ZH,
        "model_type": "DogBreedClassifier",
    }, path)


def load_checkpoint(model, path):
    model.load_state_dict(torch.load(path, map_location=DEVICE)["model_state"])


# ============================================================
# 主流程
# ============================================================

def main():
    logger.info("=" * 60)
    logger.info("犬博士 - Kaggle GPU 训练")
    logger.info(f"设备: {DEVICE}")
    logger.info(f"图片目录: {RAW_IMAGE_DIR}")
    logger.info("=" * 60)

    logger.info("加载数据集...")
    train_loader, val_loader, test_loader = create_dataloaders()

    logger.info("构建模型...")
    model = DogBreedClassifier(num_classes=NUM_CLASSES).to(DEVICE)
    criterion = nn.CrossEntropyLoss()

    history = []
    best_val_acc = 0.0
    best_model_path = MODEL_DIR / "best_model.pth"
    patience_counter = 0
    total_start = time.time()

    # Stage 1: 冻结 backbone，训练分类头
    logger.info("\nStage 1: 冻结 Backbone，训练 Classifier Head")
    freeze_backbone(model)
    optimizer = optim.AdamW(filter(lambda p: p.requires_grad, model.parameters()),
                            lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)
    scheduler = ReduceLROnPlateau(optimizer, mode="max", factor=0.5, patience=5)

    for epoch in range(1, STAGE1_EPOCHS + 1):
        train_m = train_one_epoch(model, train_loader, criterion, optimizer, epoch)
        val_m = validate(model, val_loader, criterion)
        history.append({"epoch": epoch, "stage": 1, **train_m, **val_m,
                        "lr": optimizer.param_groups[0]["lr"]})
        logger.info(f"S1 E{epoch:2d} | Train Loss: {train_m['loss']:.4f} Acc: {train_m['accuracy']:.4f} | "
                    f"Val Acc: {val_m['top1_accuracy']:.4f} Top5: {val_m['top5_accuracy']:.4f}")
        scheduler.step(val_m["top1_accuracy"])

        if val_m["top1_accuracy"] > best_val_acc:
            best_val_acc = val_m["top1_accuracy"]
            save_checkpoint(model, best_model_path)
            patience_counter = 0
        else:
            patience_counter += 1

    # Stage 2: 微调 layer4
    logger.info("\nStage 2: 解冻 layer4，微调")
    load_checkpoint(model, best_model_path)
    freeze_backbone(model, unfreeze_from="layer4")
    optimizer = optim.AdamW(filter(lambda p: p.requires_grad, model.parameters()),
                            lr=FINE_TUNE_LR, weight_decay=WEIGHT_DECAY)
    scheduler = CosineAnnealingLR(optimizer, T_max=STAGE2_EPOCHS, eta_min=FINE_TUNE_LR * 0.1)
    patience_counter = 0

    for epoch in range(STAGE1_EPOCHS + 1, STAGE1_EPOCHS + STAGE2_EPOCHS + 1):
        train_m = train_one_epoch(model, train_loader, criterion, optimizer, epoch)
        val_m = validate(model, val_loader, criterion)
        history.append({"epoch": epoch, "stage": 2, **train_m, **val_m,
                        "lr": optimizer.param_groups[0]["lr"]})
        logger.info(f"S2 E{epoch:2d} | Train Loss: {train_m['loss']:.4f} Acc: {train_m['accuracy']:.4f} | "
                    f"Val Acc: {val_m['top1_accuracy']:.4f} Top5: {val_m['top5_accuracy']:.4f}")
        scheduler.step()

        if val_m["top1_accuracy"] > best_val_acc:
            best_val_acc = val_m["top1_accuracy"]
            save_checkpoint(model, best_model_path)
            patience_counter = 0
        else:
            patience_counter += 1
        if patience_counter >= 15:
            logger.info(f"早停在 epoch {epoch}")
            break

    # Stage 3: 全量微调
    logger.info("\nStage 3: 全量微调")
    load_checkpoint(model, best_model_path)
    for param in model.parameters():
        param.requires_grad = True
    optimizer = optim.AdamW(model.parameters(), lr=FINE_TUNE_LR * 0.1, weight_decay=WEIGHT_DECAY * 0.5)
    scheduler = CosineAnnealingLR(optimizer, T_max=STAGE3_EPOCHS, eta_min=1e-6)
    patience_counter = 0

    for epoch in range(STAGE1_EPOCHS + STAGE2_EPOCHS + 1,
                       STAGE1_EPOCHS + STAGE2_EPOCHS + STAGE3_EPOCHS + 1):
        train_m = train_one_epoch(model, train_loader, criterion, optimizer, epoch)
        val_m = validate(model, val_loader, criterion)
        history.append({"epoch": epoch, "stage": 3, **train_m, **val_m,
                        "lr": optimizer.param_groups[0]["lr"]})
        logger.info(f"S3 E{epoch:2d} | Train Loss: {train_m['loss']:.4f} Acc: {train_m['accuracy']:.4f} | "
                    f"Val Acc: {val_m['top1_accuracy']:.4f} Top5: {val_m['top5_accuracy']:.4f}")
        scheduler.step()

        if val_m["top1_accuracy"] > best_val_acc:
            best_val_acc = val_m["top1_accuracy"]
            save_checkpoint(model, best_model_path)
            patience_counter = 0
        else:
            patience_counter += 1
        if patience_counter >= 15:
            logger.info(f"早停在 epoch {epoch}")
            break

    # 最终测试
    logger.info("\n" + "=" * 60)
    logger.info("最终测试集评估")
    load_checkpoint(model, best_model_path)
    test_m = validate(model, test_loader, criterion)
    total_time = time.time() - total_start

    logger.info(f"\n总训练时间: {total_time/60:.1f} 分钟")
    logger.info(f"Test Top-1: {test_m['top1_accuracy']*100:.2f}%")
    logger.info(f"Test Top-5: {test_m['top5_accuracy']*100:.2f}%")
    logger.info(f"最佳 Val Acc: {best_val_acc*100:.2f}%")

    with open(OUTPUT_DIR / "training_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "history": history,
            "test_metrics": test_m,
            "best_val_acc": best_val_acc,
            "total_time_seconds": total_time,
        }, f, indent=2, ensure_ascii=False)

    logger.info(f"\n模型已保存: {best_model_path}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
