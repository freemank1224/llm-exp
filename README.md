# 「神奇的猜词小能手」—— 给孩子的互动式大语言模型科普节目

这是一个为没有AI基础知识的小学/中学生讲解大型语言模型（LLM）预测原理的互动演示项目。旨在通过交互式页面和演示来解释LLM的工作原理。采用此项目，能够远超PPT的实时互动演示效果，生动的讲述LLM的「下一个词元预测」的工作机制。

## 安装说明

### 使用 Conda 进行环境管理

#### macOS 用户
1. 安装 Miniconda 或 Anaconda：
   访问 [Miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html) 或 [Anaconda](https://www.anaconda.com/products/distribution) 下载页面，下载并按照说明安装。
2. 创建新环境并激活：
   ```bash
   conda create --name llm-prediction python=3.9
   conda activate llm-prediction
   ```
3. 安装依赖项：
   ```bash
   pip install -r requirements.txt
   ```

#### Windows 用户
1. 安装 Miniconda 或 Anaconda：
   访问 [Miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html) 或 [Anaconda](https://www.anaconda.com/products/distribution) 下载页面，下载并按照说明安装。
2. 创建新环境并激活：
   ```bash
   conda create --name llm-prediction python=3.9
   conda activate llm-prediction
   ```
3. 安装依赖项：
   ```bash
   pip install -r requirements_win.txt
   ```

## 运行项目

### 方式一：使用Docker（推荐，一键运行）

#### 🚀 直接使用预构建镜像
```bash
# 拉取预构建的镜像（包含模型）
docker pull ghcr.io/freemank1224/llm-exp:latest

# 运行容器
docker run -d -p 8501:8501 --name llm-prediction ghcr.io/freemank1224/llm-exp:latest

# 访问应用：http://localhost:8501
```

#### 🔨 本地构建镜像
如果您想自己构建镜像：
```bash
# 克隆仓库
git clone https://github.com/freemank1224/llm-exp.git
cd llm-exp

# 构建镜像（会自动下载模型到镜像中）
./build_docker.sh

# 运行容器
./run_docker.sh
```

**Docker优势：**
- ✅ 无需安装Python环境和依赖
- ✅ 模型已预下载，启动即可使用
- ✅ 跨平台兼容（Windows/macOS/Linux）
- ✅ 一键部署，避免环境问题

### 方式二：本地Python环境运行

激活环境后，运行以下命令启动应用程序：
```bash
streamlit run Home.py
```


---
# 「Magic Token Predictor」: An interactive course of LLM prediction princeple for kids

This is an interactive demonstration project designed to explain the principles of Large Language Models (LLMs) to primary/secondary school students who have no AI background knowledge. It aims to explain how LLMs work through interactive pages and demonstrations. By utilizing this project, we can achieve real-time interactive demonstration effects far beyond PowerPoint presentations, vividly illustrating the "next token prediction" mechanism of LLMs.

## Installation Instructions

### Using Conda for Environment Management

#### macOS Users
1. Install Miniconda or Anaconda:
   Visit the [Miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html) or [Anaconda](https://www.anaconda.com/products/distribution) download page, download, and follow the instructions to install.
2. Create and activate a new environment:
   ```bash
   conda create --name llm-prediction python=3.9
   conda activate llm-prediction
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

#### Windows Users
1. Install Miniconda or Anaconda:
   Visit the [Miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html) or [Anaconda](https://www.anaconda.com/products/distribution) download page, download, and follow the instructions to install.
2. Create and activate a new environment:
   ```bash
   conda create --name llm-prediction python=3.9
   conda activate llm-prediction
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements_win.txt
   ```

## Running the Project

### Method 1: Using Docker (Recommended, One-Click Run)

#### 🚀 Use Pre-built Image
```bash
# Pull the pre-built image (with models included)
docker pull ghcr.io/freemank1224/llm-exp:latest

# Run container
docker run -d -p 8501:8501 --name llm-prediction ghcr.io/freemank1224/llm-exp:latest

# Access the app: http://localhost:8501
```

#### 🔨 Build Image Locally
If you want to build the image yourself:
```bash
# Clone repository
git clone https://github.com/freemank1224/llm-exp.git
cd llm-exp

# Build image (automatically downloads models into the image)
./build_docker.sh

# Run container
./run_docker.sh
```

**Docker Advantages:**
- ✅ No need to install Python environment and dependencies
- ✅ Models are pre-downloaded, ready to use on startup
- ✅ Cross-platform compatibility (Windows/macOS/Linux)
- ✅ One-click deployment, avoiding environment issues

### Method 2: Local Python Environment

After activating the environment, run the following command to start the application:
```bash
streamlit run Home.py
