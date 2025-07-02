# Docker 部署指南

本指南说明如何使用Docker部署LLM预测应用，模型将在构建时预下载到镜像中，避免每次启动都重新下载。

## 📋 主要改进

- ✅ **模型预下载**: 在Docker构建时下载HuggingFace模型到镜像缓存
- ✅ **多阶段构建**: 优化镜像大小，减少构建依赖
- ✅ **环境变量配置**: 正确设置HuggingFace缓存目录
- ✅ **自动化脚本**: 提供便捷的构建和运行脚本

## 🚀 快速开始

### 方法一: 使用自动化脚本（推荐）

1. **构建镜像**（首次使用或代码更新后）:
   ```bash
   ./build_docker.sh
   ```

2. **运行容器**:
   ```bash
   ./run_docker.sh
   ```

### 方法二: 手动命令

1. **构建镜像**:
   ```bash
   docker build -t llm-prediction-app:latest .
   ```

2. **运行容器**:
   ```bash
   docker run -d -p 8501:8501 --name llm-prediction-container llm-prediction-app:latest
   ```

## 📁 文件说明

- `Dockerfile`: 多阶段Docker构建配置
- `download_models.py`: 模型预下载脚本
- `build_docker.sh`: 自动化构建脚本
- `run_docker.sh`: 自动化运行脚本
- `.dockerignore`: Docker构建忽略文件

## 🔧 技术细节

### 模型缓存机制

1. **构建时下载**: 在Docker构建过程中下载Qwen2-1.5B模型
2. **缓存目录**: 模型存储在 `/app/models` 目录
3. **环境变量**: 设置HuggingFace相关环境变量指向缓存目录
4. **自动检测**: 应用自动检测Docker环境并使用正确的缓存路径

### 多阶段构建

```dockerfile
# 阶段1: 模型下载器（包含构建工具）
FROM python:3.10-slim as model-downloader
# ... 下载模型 ...

# 阶段2: 运行时镜像（精简版）
FROM python:3.10-slim
# ... 复制模型和应用文件 ...
```

### 环境变量配置

```bash
ENV HF_HOME=/app/models
ENV TRANSFORMERS_CACHE=/app/models
ENV HF_DATASETS_CACHE=/app/models
```

## 🐛 常见问题

### Q: 构建时间很长？
A: 首次构建需要下载约3GB的模型文件，这是正常的。后续构建会利用Docker缓存加速。

### Q: 如何查看容器日志？
A: 使用命令 `docker logs llm-prediction-container`

### Q: 如何停止容器？
A: 使用命令 `docker stop llm-prediction-container`

### Q: 如何更新应用？
A: 重新运行 `./build_docker.sh` 构建新镜像，然后运行 `./run_docker.sh`

## 📊 镜像大小优化

- 使用多阶段构建减少最终镜像大小
- 清理apt缓存和临时文件
- 使用 `.dockerignore` 排除不需要的文件

## 🌐 访问应用

构建并运行成功后，访问 http://localhost:8501 即可使用应用。

## ⚠️ 注意事项

1. 确保Docker有足够的存储空间（至少5GB）
2. 构建过程需要稳定的网络连接
3. 首次构建可能需要15-30分钟，取决于网络速度
