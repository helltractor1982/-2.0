"""
ResNet50 迁移学习模型 - 狗品种分类器

架构设计:
- 骨干网络: ResNet50 (ImageNet预训练)
- 分类头: 2048 -> 512 -> 120 (两层全连接 + BN + ReLU + Dropout)
- 支持多种冻结策略:
    * 不冻结(全量微调) -- 推荐用于Stanford Dogs
    * 冻结到layer3 (仅微调layer4 + classifier)
    * 完全冻结骨干 (只训练classifier)

参数量:
- ResNet50 backbone: ~23.5M
- Custom classifier: ~1.05M (2048*512 + 512 + 512*120 + 120)
- 总计: ~24.5M 参数
- 可训练参数取决于冻结策略
"""
import torch
import torch.nn as nn
import torchvision.models as models


class DogBreedClassifier(nn.Module):
    """
    基于ResNet50的狗品种分类器

    使用ImageNet预训练权重进行迁移学习,
    替换原有的全连接层为适合120类品种的分类头.

    Args:
        num_classes: 输出类别数 (Stanford Dogs = 120)
        pretrained: 是否加载ImageNet预训练权重
        dropout: 分类头中的Dropout率
        freeze_backbone: 是否完全冻结骨干网络
        freeze_until_layer: 冻结到此层(不含), 如 "layer3" 表示保留layer4可训练.
                            设为None则不冻结任何层.
    """

    def __init__(
        self,
        num_classes: int = 120,
        pretrained: bool = True,
        dropout: float = 0.5,
        freeze_backbone: bool = False,
        freeze_until_layer: str | None = None,
    ):
        super().__init__()

        # 加载预训练 ResNet50
        if pretrained:
            self.backbone = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
        else:
            self.backbone = models.resnet50(weights=None)

        # ---- 冻结策略 ----
        if freeze_backbone:
            # 完全冻结: 所有骨干参数不参与梯度计算
            for param in self.backbone.parameters():
                param.requires_grad = False

        elif freeze_until_layer is not None:
            # 选择性冻结: 冻结到指定层, 之后的层保持可训练
            # 典型: 冻结 layer1+2+3, 微调 layer4 + classifier
            freezing = True
            for name, param in self.backbone.named_parameters():
                if freeze_until_layer in name:
                    freezing = False
                param.requires_grad = not freezing

        # 获取原始fc层的输入维度
        in_features = self.backbone.fc.in_features  # 2048 for ResNet50

        # 构建新的分类头 (替代原始的单层fc)
        # 设计: GlobalAvgPool -> Dropout -> FC(2048->512) -> BN -> ReLU -> Dropout -> FC(512->num_classes)
        self.classifier = nn.Sequential(
            nn.Dropout(p=dropout),
            nn.Linear(in_features, 512),
            nn.BatchNorm1d(512),
              nn.ReLU(inplace=True),
            nn.Dropout(p=dropout * 0.6),
            nn.Linear(512, num_classes),
        )

        # 替换原有fc层为恒等映射(在forward中手动接classifier)
        self.backbone.fc = nn.Identity()

        # 初始化分类头最后一层的权重(较小的方差有助于初期收敛)
        nn.init.xavier_uniform_(self.classifier[5].weight)
        nn.init.zeros_(self.classifier[5].bias)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        前向传播

        Args:
            x: 输入图片张量 (B, 3, 224, 224)

        Returns:
            分类logits (B, num_classes)
        """
        # 通过骨干网络提取特征 (B, 2048)
        features = self.backbone(x)
        # 通过自定义分类头 (B, num_classes)
        output = self.classifier(features)
        return output

    def extract_features(self, x: torch.Tensor) -> torch.Tensor:
        """
        提取特征向量(不经过分类头)

        可用于:
        - 相似度检索
        - 特征可视化(t-SNE/UMAP)
        - 迁移到下游任务

        Args:
            x: 输入图片张量 (B, 3, 224, 224)

        Returns:
            特征向量 (B, 2048)
        """
        return self.backbone(x)

    def get_feature_dim(self) -> int:
        """返回特征维度"""
        return self.backbone.fc.in_features


def build_model(
    num_classes: int = 120,
    pretrained: bool = True,
    dropout: float = 0.5,
    freeze_strategy: str = "none",  # none / partial / full
) -> DogBreedClassifier:
    """
    工厂函数: 根据字符串配置创建模型

    Args:
        num_classes: 类别数
        pretrained: 是否使用预训练权重
        dropout: Dropout率
        freeze_strategy: 冻结策略
            "none":       -- 全量微调(推荐用于Stanford Dogs)
            "partial":    -- 冻结layer1-3, 微调layer4+classifier
            "full":       -- 只训练classifier

    Returns:
        配置好的 DogBreedClassifier 实例
    """
    if freeze_strategy == "none":
        return DogBreedClassifier(
            num_classes=num_classes,
            pretrained=pretrained,
            dropout=dropout,
            freeze_backbone=False,
            freeze_until_layer=None,
        )
    elif freeze_strategy == "partial":
        return DogBreedClassifier(
            num_classes=num_classes,
            pretrained=pretrained,
            dropout=dropout,
            freeze_backbone=False,
            freeze_until_layer="layer3",
        )
    elif freeze_strategy == "full":
        return DogBreedClassifier(
            num_classes=num_classes,
            pretrained=pretrained,
            dropout=dropout,
            freeze_backbone=True,
            freeze_until_layer=None,
        )
    else:
        raise ValueError(f"Unknown freeze_strategy: {freeze_strategy}")


def count_parameters(model: nn.Module) -> tuple[int, int]:
    """
    统计模型的参数量

    Returns:
        (total_params, trainable_params): 总参数数和可训练参数数
    """
    total = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    return total, trainable


class DogBreedClassifierFromResnet(DogBreedClassifier):
    """
    从原始 ResNet50 state_dict 构建 DogBreedClassifier。
    用于加载 Kaggle 训练格式的模型权重。
    """
    def __init__(self, num_classes: int = 120):
        super().__init__(num_classes=num_classes, pretrained=False, dropout=0.5)
        # 重置 backbone.fc 为 Identity（父类已做，这里确保）
        self.backbone.fc = nn.Identity()


class KaggleResNetClassifier(nn.Module):
    """
    与 Kaggle 实际训练的模型结构完全一致。
    
    Kaggle 实际训练使用的是:
    - ResNet50 backbone (conv1, bn1, layer1-4, avgpool)
    - 单个 fc 层: nn.Linear(2048, 120)
    
    内部使用 self.backbone (ResNet50)，state_dict key 带 backbone. 前缀。
    checkpoint 的 key 不带前缀，加载时需要添加 backbone. 前缀。
    """
    def __init__(self, num_classes: int = 120):
        super().__init__()
        self.backbone = models.resnet50(weights=None)
        in_features = self.backbone.fc.in_features  # 2048
        # 替换 fc 为 120 类输出
        self.backbone.fc = nn.Linear(in_features, num_classes)

    def forward(self, x):
        return self.backbone(x)
    
    def load_kaggle_state_dict(self, state_dict: dict):
        """
        加载 Kaggle 训练的 state_dict。
        checkpoint key 不带 backbone. 前缀，需要添加。
        """
        mapped = {}
        for k, v in state_dict.items():
            mapped[f"backbone.{k}"] = v
        self.load_state_dict(mapped)


# ======================================================
# 新版训练模型（带 CBAM 注意力机制）
# ======================================================

class _ChannelAttention(nn.Module):
    """通道注意力模块 (SENet 风格 1x1 卷积实现)"""
    def __init__(self, in_channels: int, reduction: int = 16):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Conv2d(in_channels, in_channels // reduction, 1, bias=False),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_channels // reduction, in_channels, 1, bias=False),
        )
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        avg = x.mean(dim=(2, 3), keepdim=True)
        return x * self.sigmoid(self.fc(avg))


class _SpatialAttention(nn.Module):
    """空间注意力模块"""
    def __init__(self, kernel_size: int = 7):
        super().__init__()
        self.conv = nn.Conv2d(2, 1, kernel_size, padding=kernel_size // 2, bias=False)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        avg_out = x.mean(dim=1, keepdim=True)
        max_out, _ = x.max(dim=1, keepdim=True)
        attn = torch.cat([avg_out, max_out], dim=1)
        return x * self.sigmoid(self.conv(attn))


class _CBAM(nn.Module):
    """CBAM: 先通道注意力再空间注意力"""
    def __init__(self, in_channels: int, reduction: int = 16, spatial_kernel: int = 7):
        super().__init__()
        self.ca = _ChannelAttention(in_channels, reduction)
        self.sa = _SpatialAttention(spatial_kernel)

    def forward(self, x):
        x = self.ca(x)
        x = self.sa(x)
        return x


class ResNet50CBAMClassifier(nn.Module):
    """
    新版训练模型: ResNet50 + CBAM 注意力机制 + 自定义分类头

    架构 (从 state_dict 逆向还原):
    - backbone: ResNet50 (去掉原 fc 和 avgpool 之后的结构)
    - cbam: CBAM(2048, reduction=16, spatial_kernel=7)
    - 全局平均池化: AdaptiveAvgPool2d(1)
    - fc: Sequential [Dropout, Linear(2048→512), BN(512), ReLU, Dropout, Linear(512→num_classes)]
         (索引: 0=Dropout, 1=Linear, 2=BN, 3=ReLU, 4=Dropout, 5=Linear)

    state_dict key 无前缀 (conv1.weight, layer1..., fc.1.weight, cbam...)
    """

    def __init__(self, num_classes: int = 120, dropout: float = 0.5):
        super().__init__()
        # ResNet50 backbone（保留到 layer4，去掉 avgpool 和 fc）
        resnet = models.resnet50(weights=None)
        self.conv1 = resnet.conv1
        self.bn1 = resnet.bn1
        self.relu = resnet.relu
        self.maxpool = resnet.maxpool
        self.layer1 = resnet.layer1
        self.layer2 = resnet.layer2
        self.layer3 = resnet.layer3
        self.layer4 = resnet.layer4
        self.avgpool = resnet.avgpool  # AdaptiveAvgPool2d(1)

        in_features = 2048  # ResNet50 layer4 输出通道数

        # CBAM 注意力模块 (reduction=16: 2048//16=128)
        self.cbam = _CBAM(in_channels=in_features, reduction=16, spatial_kernel=7)

        # 分类头: [Dropout(0), Linear(1), BN(2), ReLU(3), Dropout(4), Linear(5)]
        self.fc = nn.Sequential(
            nn.Dropout(p=dropout),          # 0
            nn.Linear(in_features, 512),    # 1
            nn.BatchNorm1d(512),            # 2
            nn.ReLU(inplace=True),          # 3
            nn.Dropout(p=dropout * 0.6),    # 4
            nn.Linear(512, num_classes),    # 5
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = self.cbam(x)          # CBAM 注意力
        x = self.avgpool(x)       # (B, 2048, 1, 1)
        x = torch.flatten(x, 1)  # (B, 2048)
        x = self.fc(x)            # (B, num_classes)
        return x


class EfficientNetCBAMClassifier(nn.Module):
    """
    新版 EfficientNet 训练模型: EfficientNetB0 + CBAM 注意力机制 + 自定义分类头

    架构 (从 state_dict 逆向还原):
    - features: EfficientNetB0 特征提取 (0-8)
    - cbam: CBAM(1280, reduction=16, spatial_kernel=7)
    - 全局平均池化
    - classifier: Sequential [Dropout, Linear(1280→512), BN(512), ReLU, Dropout, Linear(512→num_classes)]

    state_dict key 无前缀 (features.0..., classifier.1.weight, cbam...)
    """

    def __init__(self, num_classes: int = 120, dropout: float = 0.5):
        super().__init__()
        import torchvision.models as tv_models
        efficientnet = tv_models.efficientnet_b0(weights=None)

        self.features = efficientnet.features  # 输出 (B, 1280, H, W)
        self.avgpool = efficientnet.avgpool    # AdaptiveAvgPool2d(1)

        in_features = 1280  # EfficientNetB0 features 输出通道数

        # CBAM 注意力模块 (reduction=16: 1280//16=80)
        self.cbam = _CBAM(in_channels=in_features, reduction=16, spatial_kernel=7)

        # 分类头: [Dropout(0), Linear(1), BN(2), ReLU(3), Dropout(4), Linear(5)]
        self.classifier = nn.Sequential(
            nn.Dropout(p=dropout),            # 0
            nn.Linear(in_features, 512),      # 1
            nn.BatchNorm1d(512),              # 2
            nn.ReLU(inplace=True),            # 3
            nn.Dropout(p=dropout * 0.6),      # 4
            nn.Linear(512, num_classes),      # 5
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x)
        x = self.cbam(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x
