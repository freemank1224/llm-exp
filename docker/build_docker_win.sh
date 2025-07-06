#!/bin/bash

# Windows版Docker构建脚本
# 用于构建Windows平台下的Docker镜像

set -e  # 遇到错误立即退出

# 设置变量
IMAGE_NAME="llm-prediction-app-win"
TAG="latest"
CONTAINER_NAME="llm-prediction-container-win"

echo "🚀 开始构建Windows版本LLM预测应用Docker镜像..."

# 确认Docker Desktop已切换到Windows容器模式
echo "⚠️ 注意: 请确保Docker Desktop已切换到Windows容器模式!"
echo "   可以在Docker Desktop的设置中或通过右键点击系统托盘中的Docker图标来切换"
echo ""
read -p "是否已切换到Windows容器模式? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 请先切换到Windows容器模式再运行此脚本"
    exit 1
fi

# 检测操作系统
if [[ "$OSTYPE" == "darwin"* ]]; then
    IS_MAC=true
    echo "🖥️ 检测到macOS系统"
else
    IS_MAC=false
fi

# 构建Docker镜像
echo "📦 正在构建Windows版镜像，这可能需要一些时间..."

if [ "$IS_MAC" = true ]; then
    echo "⚠️ 警告: 在macOS上构建Windows容器可能会遇到问题"
    echo "建议: 如果遇到平台兼容性问题，请考虑在Windows机器上构建镜像"
    echo ""
    echo "正在尝试使用远程构建方式..."
    # 在macOS上尝试使用buildx和模拟器构建
    docker buildx create --name windows-builder --platform windows/amd64 --use || true
    docker buildx build --platform windows/amd64 --builder windows-builder -t ${IMAGE_NAME}:${TAG} -f docker/Dockerfile_win .
else
    # 在Windows上直接构建
    docker build -t ${IMAGE_NAME}:${TAG} -f docker/Dockerfile_win .
fi

if [ $? -eq 0 ]; then
    echo "✅ 镜像构建成功！"
    echo "📊 镜像信息："
    docker images ${IMAGE_NAME}:${TAG}
else
    echo "❌ 镜像构建失败！"
    exit 1
fi

echo ""
echo "🎯 要运行Windows容器，请使用以下命令："
echo "docker run -p 8501:8501 --name ${CONTAINER_NAME} ${IMAGE_NAME}:${TAG}"
echo ""
echo "或者运行以下脚本："
echo "./docker/run_docker_win.sh"
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
    
    echo "🚀 启动Windows容器..."
    docker run -d -p 8501:8501 --name ${CONTAINER_NAME} ${IMAGE_NAME}:${TAG}
    
    echo "✅ 容器已启动！"
    echo "🌐 应用地址: http://localhost:8501"
    echo "📋 查看日志: docker logs ${CONTAINER_NAME}"
    echo "🛑 停止容器: docker stop ${CONTAINER_NAME}"
fi
