# 使用多阶段构建优化镜像大小
FROM python:3.10-slim as model-downloader

WORKDIR /app

# 安装系统依赖（仅用于模型下载）
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements文件
COPY requirements.txt .

# 安装Python依赖
RUN pip3 install --no-cache-dir -r requirements.txt

# 设置HuggingFace缓存目录环境变量
ENV HF_HOME=/app/models
ENV TRANSFORMERS_CACHE=/app/models
ENV HF_DATASETS_CACHE=/app/models

# 创建模型缓存目录
RUN mkdir -p /app/models

# 复制模型预下载脚本
COPY download_models.py .

# 在构建时下载模型到镜像中
RUN python download_models.py

# 第二阶段：最终运行镜像
FROM python:3.10-slim

WORKDIR /app

# 安装运行时系统依赖
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements文件
COPY requirements.txt .

# 安装Python依赖
RUN pip3 install --no-cache-dir -r requirements.txt

# 设置HuggingFace缓存目录环境变量
ENV HF_HOME=/app/models
ENV TRANSFORMERS_CACHE=/app/models
ENV HF_DATASETS_CACHE=/app/models

# 从第一阶段复制下载好的模型
COPY --from=model-downloader /app/models /app/models

# 复制应用文件
COPY . .

# 暴露Streamlit端口
EXPOSE 8501

# 健康检查
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# 启动Streamlit应用
ENTRYPOINT ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]