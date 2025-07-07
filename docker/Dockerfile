# 使用多阶段构建优化镜像大小

# 第一阶段：基础镜像 - 安装共同依赖
FROM python:3.10-slim AS base
WORKDIR /app

# 设置HuggingFace缓存目录环境变量
ENV HF_HOME=/app/models
ENV TRANSFORMERS_CACHE=/app/models
ENV HF_DATASETS_CACHE=/app/models

# 复制requirements文件
COPY requirements.txt .
COPY docker/download_models.py .

# 安装Python依赖
RUN pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org --no-cache-dir -r requirements.txt

# 第二阶段：模型下载器 - 在此阶段下载模型
FROM base AS model-downloader

# 安装额外的系统依赖（仅用于模型下载）
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# 创建模型缓存目录
RUN mkdir -p /app/models

# 在构建时下载模型到镜像中
RUN python download_models.py

# 第三阶段：运行镜像 - 最终的应用镜像
FROM base

# 安装运行时所需的系统依赖
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 从第二阶段复制下载好的模型
COPY --from=model-downloader /app/models /app/models

# 复制应用文件
COPY . .

# 暴露Streamlit端口
EXPOSE 8501

# 健康检查
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# 启动Streamlit应用
ENTRYPOINT ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]