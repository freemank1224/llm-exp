#!/bin/bash

# Windows版Docker运行脚本
# 用于启动Windows平台下的Docker容器

set -e  # 遇到错误立即退出

# 设置变量
IMAGE_NAME="llm-prediction-app-win"
TAG="latest"
CONTAINER_NAME="llm-prediction-container-win"
PORT="8501"

echo "🚀 启动Windows版LLM预测应用容器..."

# 确认Docker Desktop已切换到Windows容器模式
echo "⚠️ 注意: 请确保Docker Desktop已切换到Windows容器模式!"
echo ""

# 检查镜像是否存在
if ! docker images ${IMAGE_NAME}:${TAG} | grep -q ${IMAGE_NAME}; then
    echo "❌ 镜像 ${IMAGE_NAME}:${TAG} 不存在！"
    echo "请先运行 ./docker/build_docker_win.sh 构建镜像"
    exit 1
fi

# 停止并删除已存在的容器（如果有）
if docker ps -a --format 'table {{.Names}}' | grep -q ${CONTAINER_NAME}; then
    echo "🧹 清理已存在的容器..."
    docker stop ${CONTAINER_NAME} 2>/dev/null || true
    docker rm ${CONTAINER_NAME} 2>/dev/null || true
fi

# 启动新容器
echo "📦 启动新Windows容器..."
docker run -d \
    -p ${PORT}:8501 \
    --name ${CONTAINER_NAME} \
    --restart unless-stopped \
    ${IMAGE_NAME}:${TAG}

if [ $? -eq 0 ]; then
    echo "✅ Windows容器启动成功！"
    echo ""
    echo "🌐 应用地址: http://localhost:${PORT}"
    echo "📋 查看日志: docker logs ${CONTAINER_NAME}"
    echo "📋 实时日志: docker logs -f ${CONTAINER_NAME}"
    echo "🛑 停止容器: docker stop ${CONTAINER_NAME}"
    echo "🗑️  删除容器: docker rm ${CONTAINER_NAME}"
    echo ""
    
    # 等待几秒并检查容器状态
    sleep 3
    if docker ps --format 'table {{.Names}}\t{{.Status}}' | grep -q ${CONTAINER_NAME}; then
        echo "✅ 容器运行状态正常"
        echo "🔍 正在检查应用是否就绪..."
        
        # 等待应用启动 (Windows容器启动可能较慢)
        for i in {1..60}; do
            if curl -s http://localhost:${PORT}/_stcore/health > /dev/null 2>&1; then
                echo "🎉 应用已就绪！可以访问 http://localhost:${PORT}"
                break
            fi
            echo "⏳ 等待应用启动... ($i/60)"
            sleep 3
        done
    else
        echo "❌ 容器启动失败！"
        echo "📋 查看错误日志:"
        docker logs ${CONTAINER_NAME}
        exit 1
    fi
else
    echo "❌ 容器启动失败！"
    exit 1
fi
