# 犬博士 (Dog Doctor) - 部署说明

## 环境要求

| 依赖 | 最低版本 | 说明 |
|------|---------|------|
| Python | 3.9+ | 推荐 3.11 |
| pip | 最新版 | 包管理器 |

## 快速启动（3步）

### 1. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

> ⚠️ 如果没有 NVIDIA 显卡，PyTorch 会自动安装 CPU 版本，推理稍慢但功能正常。
> 如果有 NVIDIA 显卡，建议安装 CUDA 版 PyTorch 以加速推理：
> ```bash
> pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
> ```

### 2. 双击启动

直接双击 `start.bat` 即可，脚本会：
- 自动检测项目路径（无需手动修改）
- 自动检查依赖是否已安装
- 启动后端服务（端口 8000）
- 自动打开浏览器

### 3. 访问应用

浏览器打开 `http://localhost:8000`

---

## 需要修改的地方

### ✅ 已自动适配（无需修改）

| 项目 | 说明 |
|------|------|
| 项目路径 | `start.bat` 使用 `%~dp0` 自动定位，放在任何目录都能运行 |
| 模型路径 | `main.py` 使用 `__file__` 相对路径，自动适配 |
| 前端路径 | `main.py` 使用相对路径 `../web`，自动适配 |
| ML 配置路径 | `config.py` 使用 `Path(__file__).resolve()` 自动定位 |

### ⚠️ 可能需要修改

| 文件 | 行号 | 当前值 | 何时修改 |
|------|------|--------|---------|
| `backend/ml/config.py` | 64 | `DEVICE = "cuda"` | 如果没有 NVIDIA 显卡，改为 `"cpu"`（**不改也能运行**，代码会自动降级） |

> 实际上 `inference.py` 第 39 行已有保护：`torch.device(device or (DEVICE if torch.cuda.is_available() else "cpu"))`，
> 所以即使 config 里写的 `"cuda"`，没有显卡时也会自动用 CPU，**无需手动修改**。

---

## 项目结构

```
dog-doctor/
├── start.bat              ← 双击启动（自动适配路径）
├── requirements.txt       ← Python 依赖清单
├── DEPLOY.md              ← 本说明文件
├── backend/
│   ├── main.py            ← FastAPI 后端入口
│   ├── breeds_data.py     ← 120种犬种百科数据
│   └── ml/
│       ├── config.py      ← 训练/推理配置
│       ├── model.py       ← ResNet50 模型定义
│       ├── inference.py   ← 推理引擎
│       ├── preprocess.py  ← 图像预处理
│       ├── breed_mapping.py ← 品种ID映射
│       ├── dataset.py     ← 训练数据集
│       ├── train.py       ← 训练脚本
│       └── models/
│           └── best_model.pth  ← 训练好的模型（~94MB）
└── web/
    └── index.html         ← 前端单页应用
```

---

## 常见问题

### Q: 启动后页面打不开？
检查 8000 端口是否被其他程序占用。可以在 `start.bat` 里把端口号改掉，同时修改 `backend/main.py` 最后一行的 `port=8000`。

### Q: 提示缺少模块？
运行 `pip install -r requirements.txt` 安装所有依赖。

### Q: 没有 GPU 能用吗？
完全可以。项目已内置 CPU/GPU 自动切换逻辑，没有 NVIDIA 显卡时自动使用 CPU 推理。

### Q: 想重新训练模型？
```bash
cd backend
python -m ml.train --mode full
```
训练需要 Stanford Dogs 数据集，放在 `data/stanford_dogs/` 目录下。

### Q: Mac / Linux 怎么启动？
```bash
cd backend
python main.py
```
然后浏览器打开 `http://localhost:8000`。`start.bat` 是 Windows 专用，其他系统直接运行 Python 即可。
