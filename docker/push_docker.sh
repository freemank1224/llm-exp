#!/bin/bash

# Docker 镜像推送脚本
# 用于将本地构建的镜像推送到 GitHub Container Registry

set -e  # 遇到错误立即退出

# 配置变量
GITHUB_USERNAME="freemank1224"  # 请设置您的GitHub用户名
IMAGE_NAME="llm-prediction-app"
REGISTRY="ghcr.io"
LOCAL_TAG="latest"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🚀 Docker镜像推送脚本"
echo "=================================="
echo ""
echo -e "${YELLOW}💡 使用提示：${NC}"
echo "1. 如果输入Token时无法粘贴，可以先设置环境变量："
echo "   export GITHUB_TOKEN=your_token_here"
echo "2. 或者使用以下命令直接登录："
echo "   echo your_token | docker login ghcr.io -u ${GITHUB_USERNAME} --password-stdin"
echo ""

# 检查是否设置了GitHub用户名
if [ -z "$GITHUB_USERNAME" ]; then
    echo -e "${RED}❌ 请先在脚本中设置您的GitHub用户名${NC}"
    echo "编辑 push_docker.sh 文件，设置 GITHUB_USERNAME 变量"
    exit 1
fi

# 检查本地镜像是否存在
if ! docker images ${IMAGE_NAME}:${LOCAL_TAG} | grep -q ${IMAGE_NAME}; then
    echo -e "${RED}❌ 本地镜像 ${IMAGE_NAME}:${LOCAL_TAG} 不存在！${NC}"
    echo "请先运行 ./docker/build_docker.sh 构建镜像"
    exit 1
fi

# 检查Docker登录状态
echo "🔐 检查GitHub Container Registry登录状态..."
if ! docker system info 2>/dev/null | grep -q "Username: ${GITHUB_USERNAME}"; then
    echo -e "${YELLOW}⚠️ 未登录到GitHub Container Registry${NC}"
    echo ""
    echo "请选择登录方式："
    echo "1) 使用登录助手脚本（推荐）"
    echo "2) 手动登录"
    read -p "请选择 (1/2): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[1]$ ]]; then
        echo "正在启动登录助手..."
        # 使用同目录下的login_docker.sh脚本
        ./login_docker.sh
        if [ $? -ne 0 ]; then
            echo -e "${RED}❌ 登录失败！${NC}"
            exit 1
        fi
    else
        echo ""
        echo -e "${YELLOW}💡 手动登录方法：${NC}"
        echo "1. 运行: docker login ghcr.io -u ${GITHUB_USERNAME}"
        echo "2. 或者: echo YOUR_TOKEN | docker login ghcr.io -u ${GITHUB_USERNAME} --password-stdin"
        echo "3. 或者: 先运行 ./docker/login_docker.sh 登录"
        echo ""
        echo -e "${RED}❌ 请先登录后再运行此脚本${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ 已登录到 GitHub Container Registry${NC}"
fi

# 构建远程标签
REMOTE_TAG="${REGISTRY}/${GITHUB_USERNAME}/llm-exp:${LOCAL_TAG}"
REMOTE_TAG_VERSIONED="${REGISTRY}/${GITHUB_USERNAME}/llm-exp:$(date +%Y%m%d-%H%M%S)"

echo "📦 准备推送镜像..."
echo "本地镜像: ${IMAGE_NAME}:${LOCAL_TAG}"
echo "远程标签: ${REMOTE_TAG}"
echo "版本标签: ${REMOTE_TAG_VERSIONED}"

# 给镜像打标签
echo "🏷️ 为镜像添加远程标签..."
docker tag ${IMAGE_NAME}:${LOCAL_TAG} ${REMOTE_TAG}
docker tag ${IMAGE_NAME}:${LOCAL_TAG} ${REMOTE_TAG_VERSIONED}

# 推送镜像
echo "⬆️ 推送镜像到GitHub Container Registry..."
echo "这可能需要几分钟时间，请耐心等待..."

docker push ${REMOTE_TAG}
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 推送 latest 标签成功！${NC}"
else
    echo -e "${RED}❌ 推送 latest 标签失败！${NC}"
    exit 1
fi

docker push ${REMOTE_TAG_VERSIONED}
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 推送版本标签成功！${NC}"
else
    echo -e "${RED}❌ 推送版本标签失败！${NC}"
fi

echo ""
echo "🎉 镜像推送完成！"
echo "=================================="
echo -e "${GREEN}📦 镜像地址: ${REMOTE_TAG}${NC}"
echo -e "${GREEN}📦 版本地址: ${REMOTE_TAG_VERSIONED}${NC}"
echo ""
echo "其他人现在可以使用以下命令运行您的应用："
echo "docker run -d -p 8501:8501 ${REMOTE_TAG}"
echo ""
echo "别忘了更新 README.md 中的镜像地址！"
