# 「神奇的猜词小能手」—— 给孩子的互动式大语言模型科普节目

这是一个为没有AI基础知识的学生讲解大型语言模型（LLM）预测原理的互动演示项目，**也是践行我所秉持的「AI教育必须使用AI开展」这个基本理念的系列尝试之一**。本项目基于页面和演示来解释LLM的工作原理。采用此项目，能够实现PPT无法展示的实时互动效果，生动的讲述LLM的「下一个词元预测」的工作机制。

目前项目基本成型，可以用于**互动化**演示/讲解LLM的「下一个词元预测」行为以及对应的数学原理。项目当前内容和未来的功能计划如下：

✅ 大语言模型的基本常识：什么是LLM，LLM为什么大，LLM预训练的作用等
✅ 大语言模型「下一个词元预测」基本概念和特点（互动演示）
✅ 大语言模型「下一个词元预测」的「随机性」和「创造性」（互动演示）
✅ 大语言模型「下一个词元预测」对应的数学解释：概率抽样（互动演示）
❓ 大语言模型如何读书：文本向量化、向量嵌入
❓ 大语言模型的优点和缺点
❓ 自回归预测模型之外的新进展：扩散语言模型等新技术进展

## 1. 安装说明
本项目支持两种安装方式，一个是自己部署本地环境，需要使用`Conda`命令来建立和完成Python的创建和部署；另一种是基于`Docker`，直接拉取镜像即可使用。下面分别说明。**用户在下面两种方式中选择一种即可！**

### 1.1 使用 Conda (推荐) 
使用`Conda`环境部署可以更清晰的了解代码结构，并方便学习者自定义模型或页面。

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
使用`Docker`作为部署方式，可以避免环境配置的问题，并快速启动服务。只需要按照下一节`2.2`中所描述的方法拉取镜像文件，并启动即可。

> ⚠️ 注意：不同平台（Windows/Linux/macOS）对应的镜像文件是不同的，混用会出现性能下降甚至无法运行的情况，因此需要根据自己的平台来选择对应的镜像，综合看来，反而并没有方便多少，因此这里还是推荐上面第一种方式，直接使用`Conda`环境进行部署！

**目前构建的镜像：**
- ✅ 苹果系统macOS with Apple M1/M2/M3/M4
- ✅ Linux with x86_64
- ❌ Windows with x86_64 还未完成构建

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

#### 🚀 使用预构建镜像(不建议初学者尝试或使用)


```bash
# 拉取预构建的镜像（包含模型）
docker pull ghcr.io/freemank1224/llm-exp:latest

# 运行容器
docker run -d -p 8501:8501 --name llm-prediction ghcr.io/freemank1224/llm-exp:latest

# 访问应用：http://localhost:8501
```

#### 🔨 本地构建镜像
⚠️ 这部分仅对于想构建自己系统镜像的使用者而准备。**对于初学者而言，直接使用预构建的镜像即可，无需自己构建镜像。**
包括`Dockerfile`在内，所有的文件都放在项目的`/docker`目录下。这里只列出在MacOS下的构建方法（Linux可能也适用，但未做验证），其它平台请自行搜索和尝试：

```bashß
# 克隆仓库
git clone https://github.com/freemank1224/llm-exp.git
cd llm-exp/docker

# 构建镜像（会自动下载模型到镜像中）
./docker/build_docker.sh

# 运行容器
./docker/run_docker.sh
```






---
# 「Magic Token Predictor」: An interactive course of LLM prediction principle for kids

This is an interactive demonstration project designed to explain the principles of Large Language Models (LLMs) to primary/secondary school students who have no AI background knowledge. **It is also one of my series of attempts to practice the basic educational philosophy of "AI education must use AI."** This project explains the working principles of LLMs through interactive pages and demonstrations. By utilizing this project, we can achieve real-time interactive effects that PowerPoint cannot demonstrate, vividly illustrating the "next token prediction" mechanism of LLMs.

The project is currently well-developed and can be used for **interactive** demonstrations/explanations of LLM's "next token prediction" behavior and its corresponding mathematical principles. The current content and future feature plans of the project are as follows:

✅ Basic knowledge of large language models: What is an LLM, why is it "large," and the role of LLM pre-training, etc.  
✅ Basic concepts and characteristics of LLM's "next token prediction" (interactive demonstration)  
✅ The "randomness" and "creativity" of LLM's "next token prediction" (interactive demonstration)  
✅ Mathematical explanation corresponding to LLM's "next token prediction": probabilistic sampling (interactive demonstration)  
❓ How LLMs read: text vectorization, vector embedding  
❓ Advantages and disadvantages of LLMs  
❓ Advances beyond autoregressive prediction models: new technologies such as diffusion language models  


## 1. Installation Instructions
This project supports two installation methods: one is to deploy the local environment yourself, which requires using `Conda` commands to create and deploy Python; the other is based on `Docker`, where you can directly pull the image to use. The following explains each method separately. **Users only need to choose one of these two methods!**

### 1.1 Using Conda (Recommended)
Using the `Conda` environment for deployment allows for a clearer understanding of the code structure and makes it easier for learners to customize models or pages.

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
Using `Docker` as a deployment method can avoid environment configuration issues and quickly start the service. You only need to follow the methods described in the next section `2.2` to pull the image file and start it.

> ⚠️ Note: Different platforms (Windows/Linux/macOS) correspond to different image files, and mixing them will result in performance degradation or even failure to run. Therefore, you need to choose the corresponding image according to your platform. Overall, this is not much more convenient, so we recommend using the first method above, directly deploying with the `Conda` environment!

**Currently built images:**
- ✅ macOS with Apple M1/M2/M3/M4
- ✅ Linux with x86_64
- ❌ Windows with x86_64 not yet completed

**Installing Docker Environment**
Before using Docker, you need to install Docker Desktop on your computer:

1. Visit [Docker Desktop Official Website](https://www.docker.com/products/docker-desktop/) to download Docker Desktop for your operating system
2. Follow the installation wizard to complete the installation
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

#### 🚀 Using Pre-built Image (Not recommended for beginners)
```bash
# Pull the pre-built image (with models included)
docker pull ghcr.io/freemank1224/llm-exp:latest

# Run container
docker run -d -p 8501:8501 --name llm-prediction ghcr.io/freemank1224/llm-exp:latest

# Access the app: http://localhost:8501
```

#### 🔨 Build Image Locally
⚠️ This part is only prepared for users who want to build their own system images. **For beginners, using the pre-built image is sufficient, and there's no need to build the image yourself.**
All files, including the `Dockerfile`, are located in the project's `/docker` directory. Here only lists the build method for macOS (Linux may also apply, but not verified). For other platforms, please search and try by yourself:

```bash
# Clone repository
git clone https://github.com/freemank1224/llm-exp.git
cd llm-exp/docker

# Build image (automatically downloads models into the image)
./docker/build_docker.sh

# Run container
./docker/run_docker.sh
```
