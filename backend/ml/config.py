"""
模型训练与推理配置常量
"""

from pathlib import Path

# ====== 路径配置 ======
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # dog-doctor/
DATA_DIR = BASE_DIR / "data" / "stanford_dogs"
IMAGE_DIR = DATA_DIR / "images" / "Images"
ANNOTATION_DIR = DATA_DIR / "annotations" / "Annotation"
MODEL_DIR = BASE_DIR / "backend" / "ml" / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = MODEL_DIR / "best_model.pth"
HISTORY_PATH = MODEL_DIR / "training_history.json"
CONFUSION_PATH = MODEL_DIR / "confusion_matrix.npy"
CLASS_NAMES_PATH = MODEL_DIR / "class_names.json"

# ====== 图像预处理 ======
IMAGE_SIZE = 224              # 输入尺寸 (ResNet50 标准)
RESIZE_SIZE = 256             # 训练时先 Resize 再 RandomCrop
MEAN = [0.485, 0.456, 0.406]  # ImageNet 均值
STD = [0.229, 0.224, 0.225]   # ImageNet 标准差

# ====== 数据增强 ======
AUGMENTATION = {
    "random_horizontal_flip": 0.5,
    "random_rotation": 15,      # 度数
    "brightness_jitter": 0.2,
    "contrast_jitter": 0.2,
    "saturation_jitter": 0.2,
    "hue_jitter": 0.1,
}

# ====== 数据集划分 ======
TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15

# ====== 训练配置 ======
BATCH_SIZE = 32
NUM_EPOCHS = 30
NUM_WORKERS = 0              # Windows 下设为0避免多进程开销
LEARNING_RATE = 0.001
FINE_TUNE_LR = 0.0001
WEIGHT_DECAY = 1e-4
MOMENTUM = 0.9

# 两阶段训练
STAGE1_EPOCHS = 3            # 冻结 backbone，训练 classifier head
STAGE2_EPOCHS = 7            # 解冻最后几层，微调

# 学习率调度
LR_PATIENCE = 5              # ReduceLROnPlateau 耐心值
LR_FACTOR = 0.5              # 学习率衰减因子

# 早停
EARLY_STOP_PATIENCE = 10

# ====== 推理配置 ======
TOP_K = 5                    # 默认返回 Top-K 结果
CONFIDENCE_THRESHOLD = 0.1   # 最低置信度阈值
DEVICE = "cuda"              # 推理设备: "cuda" | "cpu"
USE_HALF_PRECISION = False   # 是否使用 FP16 (仅 CUDA)

# ====== 可视化 ======
CHART_DIR = MODEL_DIR / "charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)
