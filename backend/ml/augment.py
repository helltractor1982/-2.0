"""
高级图像增强策略

针对Stanford Dogs小样本特点(~171张/类)设计的增强方法:

1. MixUp: 混合两张图片及对应标签, 提升模型泛化能力
2. CutMix: 将一张图的矩形区域裁剪并替换为另一张图
3. RandomErasing: 随机擦除图像中的矩形区域(模拟遮挡)

使用方式:
    在 train.py 的 train_epoch 中按概率选择增强策略
    默认: 50% MixUp / 30% CutMix / 20% 无增强(正常训练)
"""
import numpy as np
import torch


def mixup_data(x: torch.Tensor, y: torch.Tensor, alpha: float = 0.2):
    """
    MixUp 数据增强

    将两张图片按lambda比例混合, 同时混合其one-hot标签

    Args:
        x: 输入图片批次 (B, C, H, W)
        y: 标签批次 (B,)
        alpha: Beta分布的浓度参数(alpha越大lambda越接近0.5)

    Returns:
        mixed_x: 混合后的图片 (B, C, H, W)
        y_a: 原始标签 (B,)
        y_b: 混合目标的标签 (B,)
        lam: 混合系数 (标量或tensor)
    """
    if alpha > 0:
        lam = np.random.beta(alpha, alpha)
    else:
        lam = alpha

    batch_size = x.size(0)
    index = torch.randperm(batch_size).to(x.device)

    mixed_x = lam * x + (1 - lam) * x[index, :]
    y_a, y_b = y, y[index]

    return mixed_x, y_a, y_b, lam


def cutmix_data(x: torch.Tensor, y: torch.Tensor, alpha: float = 1.0):
    """
    CutMix 数据增强

    从另一张图中裁剪一个随机矩形区域覆盖到当前图上,
    同时按区域面积比例混合标签

    Args:
        x: 输入图片批次 (B, C, H, W)
        y: 标签批次 (B,)
        alpha: Beta分布浓度参数

    Returns:
        mixed_x: 剪切混合后的图片
        y_a: 原始标签
        y_b: 被裁剪区域的来源标签
        lam: 有效混合比例(基于实际裁剪面积)
    """
    if alpha > 0:
        lam = np.random.beta(alpha, alpha)
    else:
        lam = alpha

    batch_size = x.size(0)
    index = torch.randperm(batch_size).to(x.device)

    # 生成随机裁剪矩形
    cut_rat = np.sqrt(1.0 - lam)
    cut_w = int(x.size(2) * cut_rat)
    cut_h = int(x.size(3) * cut_rat)

    # 随机中心点
    cx = np.random.randint(x.size(2))
    cy = np.random.randint(x.size(3))

    # 计算边界框坐标(钳制在图像范围内)
    bbx1 = int(np.clip(cx - cut_w // 2, 0, x.size(2)))
    bby1 = int(np.clip(cy - cut_h // 2, 0, x.size(3)))
    bbx2 = int(np.clip(cx + cut_w // 2, 0, x.size(2)))
    bby2 = int(np.clip(cy + cut_h // 2, 0, x.size(3)))

    # 执行区域替换
    mixed_x = x.clone()
    mixed_x[:, :, bbx1:bbx2, bby1:bby2] = x[index, :, bbx1:bbx2, bby1:bby2]

    # 调整lam为实际替换面积比
    adjusted_lam = 1.0 - ((bbx2 - bbx1) * (bby2 - bby1) / (x.size(2) * x.size(3)))

    return mixed_x, y, y[index], adjusted_lam


def random_erasing(
    x: torch.Tensor,
    p: float = 0.5,
    scale: tuple = (0.02, 0.33),
    ratio: tuple = (0.3, 3.3),
    value: float = 0.0,
) -> torch.Tensor:
    """
    Random Erasing (随机擦除/隐藏) 数据增强

    以概率p随机擦除图像中的一个矩形区域,
    用均值/随机值填充, 模拟真实场景中的遮挡情况

    Args:
        x: 输入图片 (B, C, H, W) 或单张 (C, H, W)
        p: 执行擦除的概率
        scale: 擦除区域面积占图像总面积的比例范围
        ratio: 擦除区域的宽高比范围
        value: 擦除区域的填充值(0表示用随机噪声填充)

    Returns:
        处理后的图片(可能未修改, 取决于概率p)
    """
    if torch.rand(1).item() > p:
        return x

    if x.dim() == 3:
        x = x.unsqueeze(0)  # (C,H,W) -> (1,C,H,W)
        single = True
    else:
        single = False

    _, _, h, w = x.shape

    # 随机生成擦除区域参数
    erase_area = w * h * (scale[0] + torch.rand(1).item() * (scale[1] - scale[0]))
    aspect_ratio = ratio[0] + torch.rand(1).item() * (ratio[1] - ratio[0])

    erase_h = int(round(np.sqrt(erase_area * aspect_ratio)))
    erase_w = int(round(np.sqrt(erase_area / aspect_ratio)))
    erase_h = min(erase_h, h - 1)
    erase_w = min(erase_w, w - 1)

    if erase_h < 1 or erase_w < 1:
        return x.squeeze(0) if single else x

    # 随机位置
    top = int(torch.randint(0, h - erase_h, (1,)).item())
    left = int(torch.randint(0, w - erase_w, (1,)).item())

    # 创建输出副本
    erased = x.clone()
    if value == 0:
        # 用随机值填充
        erased[:, :, top:top+erase_h, left:left+erase_w] = torch.randn_like(
            erased[:, :, top:top+erase_h, left:left+erase_w]
        )
    else:
        erased[:, :, top:top+erase_h, left:left+erase_w] = value

    return erased.squeeze(0) if single else erased


def mixup_criterion(
    criterion: torch.nn.Module,
    pred: torch.Tensor,
    y_a: torch.Tensor,
    y_b: torch.Tensor,
    lam: float,
) -> torch.Tensor:
    """
    MixUp/CutMix 的损失函数

    按照混合比例加权两个标签的交叉熵损失

    Args:
        criterion: 损失函数(通常是CrossEntropyLoss)
        pred: 模型预测输出 (B, num_classes)
        y_a: 第一组标签 (B,)
        y_b: 第二组标签 (B,)
        lam: 混合系数

    Returns:
        加权损失值 (标量)
    """
    return lam * criterion(pred, y_a) + (1 - lam) * criterion(pred, y_b)


class AugmentationScheduler:
    """
    增强策略调度器

    在训练过程中动态调整增强强度和类型
    例如: 初期多用MixUp, 后期减少增强以精细收敛

    Usage:
        aug_scheduler = AugmentationScheduler(total_epochs=50)
        for epoch in range(50):
            strategy, params = aug_scheduler.get_strategy(epoch)
            # 在训练循环中使用strategy
    """

    def __init__(
        self,
        total_epochs: int = 50,
        mixup_prob: float = 0.5,
        cutmix_prob: float = 0.3,
        mixup_alpha_start: float = 0.4,
        mixup_alpha_end: float = 0.1,
        erase_p: float = 0.2,
    ):
        self.total_epochs = total_epochs
        self.mixup_prob = mixup_prob
        self.cutmix_prob = cutmix_prob
        self.mixup_alpha_start = mixup_alpha_start
        self.mixup_alpha_end = mixup_alpha_end
        self.erase_p = erase_p

    def get_strategy(self, epoch: int) -> tuple:
        """
        获取当前epoch应该使用的增强策略

        Returns:
            (strategy_name, kwargs): 策略名称及其参数
        """
        progress = epoch / self.total_epochs

        # 随训练进行逐渐降低增强强度(linear decay)
        current_mixup_alpha = (
            self.mixup_alpha_start
            + (self.mixup_alpha_end - self.mixup_alpha_start) * progress
        )

        r = torch.rand(1).item()

        # 前70% epoch主要使用MixUp/CutMix, 后30%减少
        if epoch < self.total_epochs * 0.7:
            if r < self.mixup_prob:
                return ("mixup", {"alpha": current_mixup_alpha})
            elif r < self.mixup_prob + self.cutmix_prob:
                return ("cutmix", {"alpha": 1.0})
            else:
                return ("none", {})
        else:
            # 后期只用RandomErasing或不增强
            if r < 0.15:
                return ("mixup", {"alpha": self.mixup_alpha_end})
            elif r < 0.25:
                return ("cutmix", {"alpha": 0.5})
            else:
                return ("none", {})
