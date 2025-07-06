#!/bin/bash

# Docker 构建和运行脚本
# 用于构建包含模型缓存的Docker镜像

set -e  # 遇到错误立即退出

# 设置变量
IMAGE_NAME="llm-prediction-app"
TAG="latest"
CONTAINER_NAME="llm-prediction-container"

echo "🚀 开始构建LLM预测应用Docker镜像..."

# 构建Docker镜像
echo "📦 正在构建镜像，这可能需要一些时间来下载模型..."
docker build -t ${IMAGE_NAME}:${TAG} -f docker/Dockerfile .

if [ $? -eq 0 ]; then
    echo "✅ 镜像构建成功！"
    echo "📊 镜像信息："
    docker images ${IMAGE_NAME}:${TAG}
else
    echo "❌ 镜像构建失败！"
    exit 1
fi

echo ""
echo "🎯 要运行容器，请使用以下命令："
echo "docker run -p 8501:8501 --name ${CONTAINER_NAME} ${IMAGE_NAME}:${TAG}"
echo ""
echo "或者运行以下脚本："
echo "./docker/run_docker.sh"
echo ""

# 询问是否立即运行
read -p "是否要立即运行容器？(y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 停止并删除已存在的容器（如果有）
    if docker ps -a --format 'table {{.Names}}' | grep -q ${CONTAINER_NAME}; then
        echo "🧹 清理已存在的容器..."
        docker stop ${CONTAINER_NAME} 2>/dev/null || true
        docker rm ${CONTAINER_NAME} 2>/dev/null || true
    fi
    
    echo "🚀 启动容器..."
    docker run -d -p 8501:8501 --name ${CONTAINER_NAME} ${IMAGE_NAME}:${TAG}
    
    echo "✅ 容器已启动！"
    echo "🌐 应用地址: http://localhost:8501"
    echo "📋 查看日志: docker logs ${CONTAINER_NAME}"
    echo "🛑 停止容器: docker stop ${CONTAINER_NAME}"
fi
