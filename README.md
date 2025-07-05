# 「神奇的猜词小能手」—— 给孩子的互动式大语言模型科普节目

这是一个为没有AI基础知识的小学/中学生讲解大型语言模型（LLM）预测原理的互动演示项目。旨在通过交互式页面和演示来解释LLM的工作原理。采用此项目，能够远超PPT的实时互动演示效果，生动的讲述LLM的「下一个词元预测」的工作机制。

## 1. 安装说明
本项目支持两种安装方式，一个是自己部署本地环境，需要使用`Conda`命令来建立和完成Python的创建和部署；另一种是基于`Docker`，直接拉取镜像即可使用。下面分别说明。

### 1.1 使用 Conda 

#### MacOS 用户（应该也适用于Ubuntu用户，但并未经过验证）
1. 用户计算机中必须存在Conda环境，如果没有，需要先安装 Miniconda 或 Anaconda：
   访问 [Miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html) 或 [Anaconda](https://www.anaconda.com/products/distribution) 下载页面，下载并按照说明安装。
2. 创建新环境并激活：
   ```bash
   conda create --name llm-prediction python=3.10
   conda activate llm-prediction
   ```
3. 安装依赖项：
   ```bash
   pip install -r requirements.txt
   ```

#### Windows 用户
1. 用户计算机中必须存在Conda环境，如果没有，需要先安装 Miniconda 或 Anaconda：
   访问 [Miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html) 或 [Anaconda](https://www.anaconda.com/products/distribution) 下载页面，下载并按照说明安装。
2. 创建新环境并激活：
   ```bash
   conda create --name llm-prediction python=3.10
   conda activate llm-prediction
   ```
3. 安装依赖项：
   ```bash
   pip install -r requirements_win.txt
   ```

### 1.2 使用 Docker
**使用Docker的优势：**
- ✅ 无需安装Python环境和依赖
- ✅ 模型已预下载，启动即可使用
- ✅ 跨平台兼容（Windows/macOS/Linux）
- ✅ 一键部署，避免环境问题

**安装 Docker 环境**
在使用 Docker 方式之前，您需要先在计算机上安装 Docker Desktop：

1. 访问 [Docker Desktop 官网](https://www.docker.com/products/docker-desktop/) 下载适合您操作系统的 Docker Desktop
2. 按照安装向导完成安装
3. 安装完成后启动 Docker Desktop
4. 等待 Docker 引擎完全启动（托盘图标变为运行状态）

安装完成后，您就可以按照下一节中的步骤拉取和运行项目镜像了。

> **注意**：Docker Desktop 支持 Windows 10/11 Pro/Enterprise/Education 和 macOS 10.15+，其他系统版本可能需要使用 Docker Toolbox 或其他替代方案。

## 2. 运行项目

### 2.1 本地Python环境运行（在1.1节Conda环境配置完成之后）
以下步骤对于Windows系统还是MacOS系统均适用。只不过MacOS是在终端（Terminal）中执行，Windows是在命令提示符（Anaconda Prompt）中执行。

- 激活环境
  ```bash
  conda activate llm-prediction
  ```

- 切换到项目目录下，运行以下命令启动应用程序
  ```bash
  cd ～/Documents/llm-exp
  streamlit run Home.py
  ```

### 2.2 使用 Docker（对应1.2节Docker环境配置完成的情况）

#### 🚀 使用预构建镜像
```bash
# 拉取预构建的镜像（包含模型）
docker pull ghcr.io/freemank1224/llm-exp:latest

# 运行容器
docker run -d -p 8501:8501 --name llm-prediction ghcr.io/freemank1224/llm-exp:latest

# 访问应用：http://localhost:8501
```

#### 🔨 本地构建镜像
如果您要尝试自己构建镜像，这里只列出在MacOS下的构建方法（Linux可能也适用，但未做验证），其它平台请自行搜索和尝试：
```bash
# 克隆仓库
git clone https://github.com/freemank1224/llm-exp.git
cd llm-exp

# 构建镜像（会自动下载模型到镜像中）
./build_docker.sh

# 运行容器
./run_docker.sh
```






---
# 「Magic Token Predictor」: An interactive course of LLM prediction principle for kids

This is an interactive demonstration project designed to explain the principles of Large Language Models (LLMs) to primary/secondary school students who have no AI background knowledge. It aims to explain how LLMs work through interactive pages and demonstrations. By utilizing this project, we can achieve real-time interactive demonstration effects far beyond PowerPoint presentations, vividly illustrating the "next token prediction" mechanism of LLMs.

## 1. Installation Instructions
This project supports two installation methods: one is to deploy the local environment yourself, which requires using `Conda` commands to create and deploy Python; the other is based on `Docker`, where you can directly pull the image to use. The following explains each method separately.

### 1.1 Using Conda

#### macOS Users (should also apply to Ubuntu users, but not verified)
1. The user's computer must have a Conda environment. If not, you need to install Miniconda or Anaconda first:
   Visit the [Miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html) or [Anaconda](https://www.anaconda.com/products/distribution) download page, download, and follow the instructions to install.
2. Create and activate a new environment:
   ```bash
   conda create --name llm-prediction python=3.10
   conda activate llm-prediction
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

#### Windows Users
1. The user's computer must have a Conda environment. If not, you need to install Miniconda or Anaconda first:
   Visit the [Miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html) or [Anaconda](https://www.anaconda.com/products/distribution) download page, download, and follow the instructions to install.
2. Create and activate a new environment:
   ```bash
   conda create --name llm-prediction python=3.10
   conda activate llm-prediction
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements_win.txt
   ```

### 1.2 Using Docker
**Advantages of using Docker:**
- ✅ No need to install Python environment and dependencies
- ✅ Models are pre-downloaded, ready to use on startup
- ✅ Cross-platform compatibility (Windows/macOS/Linux)
- ✅ One-click deployment, avoiding environment issues

**Installing Docker Environment**
Before using Docker, you need to install Docker Desktop on your computer:

1. Visit [Docker Desktop Official Website](https://www.docker.com/products/docker-desktop/) to download Docker Desktop for your operating system
2. Complete the installation following the installation wizard
3. Launch Docker Desktop after installation
4. Wait for the Docker engine to fully start (tray icon shows running status)

After installation is complete, you can follow the steps in the next section to pull and run the project image.

> **Note**: Docker Desktop supports Windows 10/11 Pro/Enterprise/Education and macOS 10.15+. Other system versions may need to use Docker Toolbox or other alternatives.

## 2. Running the Project

### 2.1 Local Python Environment (After completing Conda environment configuration in Section 1.1)
The following steps apply to both Windows and macOS systems. The only difference is that macOS executes in Terminal, while Windows executes in Command Prompt (Anaconda Prompt).

- Activate environment
  ```bash
  conda activate llm-prediction
  ```

- Switch to the project directory and run the following command to start the application
  ```bash
  cd ~/Documents/llm-exp
  streamlit run Home.py
  ```

### 2.2 Using Docker (Corresponding to Docker environment configuration completed in Section 1.2)

#### 🚀 Using Pre-built Image
```bash
# Pull the pre-built image (with models included)
docker pull ghcr.io/freemank1224/llm-exp:latest

# Run container
docker run -d -p 8501:8501 --name llm-prediction ghcr.io/freemank1224/llm-exp:latest

# Access the app: http://localhost:8501
```

#### 🔨 Build Image Locally
If you want to try building the image yourself, here only lists the build method for macOS (Linux may also apply, but not verified). For other platforms, please search and try by yourself:
```bash
# Clone repository
git clone https://github.com/freemank1224/llm-exp.git
cd llm-exp

# Build image (automatically downloads models into the image)
./build_docker.sh

# Run container
./run_docker.sh
```
