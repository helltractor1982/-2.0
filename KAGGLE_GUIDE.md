# Kaggle Notebook 训练指南 — 犬博士

## 步骤 1: 注册 Kaggle 账号
1. 打开 https://www.kaggle.com/
2. 点击右上角 "Register" 注册（可用 Google 账号）
3. 完成手机验证（需要接收验证码）

## 步骤 2: 创建 Notebook
1. 点击左侧菜单 "Code" → "New Notebook"
2. 在右侧面板 "Accelerator" 选择 **GPU T4 x2**
3. "Internet" 打开（需要下载预训练权重）

## 步骤 3: 添加数据集
1. 点击右侧 "Add Input" → 搜索 "stanford dogs"
2. 选择 **"Stanford Dogs Dataset"**（或包含 stanford-dogs 的数据集）
3. 添加后数据集会挂载到 `/kaggle/input/`

## 步骤 4: 上传训练脚本并运行
在 Notebook 的第一个 cell 中运行：

```python
# Cell 1: 上传并运行训练脚本
!pip install tqdm -q

# 复制训练脚本到工作目录
import shutil, os

# 方式A: 如果你已上传 kaggle_train.py
# !python kaggle_train.py

# 方式B: 直接把脚本代码粘贴到下一个 cell 运行
```

然后新建一个 cell，把 `kaggle_train.py` 的**全部内容**复制粘贴进去运行。

**或者更简单的方法：**

1. 在 Kaggle Notebook 右侧点击 "Upload" 上传 `kaggle_train.py`
2. 在 cell 中运行：`!python kaggle_train.py`

## 步骤 5: 修改数据集路径（如果需要）
如果数据集名称不同，脚本会自动检测，也可以手动修改 `STANFORD_DOGS_DIR` 变量。

查看数据集实际路径：
```python
!ls /kaggle/input/
```

## 步骤 6: 下载训练结果
训练完成后，在 Notebook 最后添加：

```python
from IPython.display import FileLink
FileLink("dog_doctor_output/models/best_model.pth")
```

点击链接下载模型文件，放到本地项目的 `backend/ml/models/` 目录。

## 训练时间预估 (T4 GPU)

| 阶段 | Epochs | 预估时间 |
|---|---|---|
| Stage 1 (分类头) | 5 | ~2分钟 |
| Stage 2 (微调layer4) | 15 | ~8分钟 |
| Stage 3 (全量微调) | 30 | ~20分钟 |
| **合计** | **50** | **约30分钟** |

## 预期结果
- Top-1 验证准确率: 85-92%
- Top-5 验证准确率: 97-99%
- 模型大小: ~100MB (.pth)

## 常见问题

**Q: 提示显存不足？**
A: 将 `BATCH_SIZE` 从 32 改为 16。

**Q: 找不到数据集？**
A: 检查 `/kaggle/input/` 目录，修改 `STANFORD_DOGS_DIR` 路径。

**Q: 下载预训练权重失败？**
A: 确保右侧 "Internet" 开关已打开。

**Q: 怎么把模型用在本地项目？**
A: 下载 `best_model.pth`，放到 `E:\dog_doctor\dog-doctor\backend\ml\models\` 目录。
