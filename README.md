# LLM 预测项目

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
激活环境后，运行以下命令启动应用程序：
```bash
streamlit run Home.py
```


---
# LLM Prediction Project

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
After activating the environment, run the following command to start the application:
```bash
streamlit run Home.py
