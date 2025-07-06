#!/bin/bash

# 快速部署脚本 - 使用预构建的Docker镜像
# 适用于想要快速体验应用的用户

set -e

# 配置
GITHUB_USERNAME="freemank1224"  # 请替换为实际的GitHub用户名
IMAGE_NAME="ghcr.io/${GITHUB_USERNAME}/llm-exp:latest"
CONTAINER_NAME="llm-prediction-app"
PORT="8501"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🚀 LLM预测应用快速部署脚本${NC}"
echo "=================================="
echo "镜像: ${IMAGE_NAME}"
echo "端口: ${PORT}"
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker未安装！请先安装Docker Desktop${NC}"
    echo "下载地址: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# 检查Docker是否运行
if ! docker info &> /dev/null; then
    echo -e "${RED}❌ Docker未运行！请启动Docker Desktop${NC}"
    exit 1
fi

# 检查端口是否被占用
if lsof -Pi :${PORT} -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️ 端口 ${PORT} 已被占用${NC}"
    read -p "是否使用其他端口？输入新端口号（直接回车使用8502）: " NEW_PORT
    if [ -z "$NEW_PORT" ]; then
        PORT="8502"
    else
        PORT="$NEW_PORT"
    fi
    echo "使用端口: ${PORT}"
fi

# 停止并删除已存在的容器
if docker ps -a --format 'table {{.Names}}' | grep -q ${CONTAINER_NAME}; then
    echo -e "${YELLOW}🧹 清理已存在的容器...${NC}"
    docker stop ${CONTAINER_NAME} 2>/dev/null || true
    docker rm ${CONTAINER_NAME} 2>/dev/null || true
fi

# 拉取最新镜像
echo -e "${BLUE}📦 拉取最新镜像...${NC}"
echo "这可能需要几分钟时间，请耐心等待..."
docker pull ${IMAGE_NAME}

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ 镜像拉取失败！${NC}"
    echo "可能的原因："
    echo "1. 网络连接问题"
    echo "2. 镜像不存在或无权访问"
    echo "3. GitHub用户名设置错误"
    exit 1
fi

# 运行容器
echo -e "${BLUE}🚀 启动应用容器...${NC}"
docker run -d \
    -p ${PORT}:8501 \
    --name ${CONTAINER_NAME} \
    --restart unless-stopped \
    ${IMAGE_NAME}

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 容器启动成功！${NC}"
    echo ""
    
    # 等待应用启动
    echo -e "${BLUE}🔍 等待应用启动...${NC}"
    for i in {1..30}; do
        if curl -s http://localhost:${PORT}/_stcore/health > /dev/null 2>&1; then
            echo -e "${GREEN}🎉 应用已就绪！${NC}"
            break
        fi
        echo -e "${YELLOW}⏳ 启动中... ($i/30)${NC}"
        sleep 3
    done
    
    echo ""
    echo "=================================="
    echo -e "${GREEN}🌐 应用地址: http://localhost:${PORT}${NC}"
    echo ""
    echo "📋 管理命令:"
    echo "  查看日志: docker logs ${CONTAINER_NAME}"
    echo "  实时日志: docker logs -f ${CONTAINER_NAME}"
    echo "  停止应用: docker stop ${CONTAINER_NAME}"
    echo "  重启应用: docker restart ${CONTAINER_NAME}"
    echo "  删除应用: docker stop ${CONTAINER_NAME} && docker rm ${CONTAINER_NAME}"
    echo ""
    echo -e "${BLUE}💡 提示: 如果要完全删除，还需要删除镜像：${NC}"
    echo "  docker rmi ${IMAGE_NAME}"
    echo ""
    
    # 尝试打开浏览器
    if command -v open &> /dev/null; then
        read -p "是否现在打开浏览器？(y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            open http://localhost:${PORT}
        fi
    elif command -v xdg-open &> /dev/null; then
        read -p "是否现在打开浏览器？(y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            xdg-open http://localhost:${PORT}
        fi
    fi
    
else
    echo -e "${RED}❌ 容器启动失败！${NC}"
    echo "查看错误日志:"
    docker logs ${CONTAINER_NAME} 2>/dev/null || echo "无法获取日志"
    exit 1
fi
