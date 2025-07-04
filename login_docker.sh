#!/bin/bash

# Docker GHCR 登录脚本
# 专门用于登录 GitHub Container Registry

set -e

# 配置
GITHUB_USERNAME="freemank1224"
REGISTRY="ghcr.io"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔐 GitHub Container Registry 登录助手${NC}"
echo "==========================================="
echo ""

# 检查是否已经登录
if docker system info 2>/dev/null | grep -q "Username: ${GITHUB_USERNAME}"; then
    echo -e "${GREEN}✅ 您已经登录到 ${REGISTRY}${NC}"
    echo "用户名: ${GITHUB_USERNAME}"
    exit 0
fi

echo -e "${YELLOW}📋 获取GitHub Personal Access Token步骤：${NC}"
echo "1. 访问: https://github.com/settings/tokens"
echo "2. 点击 'Generate new token (classic)'"
echo "3. 选择权限: write:packages, read:packages"
echo "4. 复制生成的token"
echo ""

echo -e "${BLUE}💡 登录方法选择：${NC}"
echo "1) 从环境变量读取Token（推荐）"
echo "2) 从文件读取Token"
echo "3) 手动输入Token"
echo "4) 显示手动登录命令"

read -p "请选择方法 (1-4): " -n 1 -r
echo
echo

case $REPLY in
    1)
        if [ -n "$GITHUB_TOKEN" ]; then
            echo -e "${GREEN}✅ 从环境变量 GITHUB_TOKEN 读取Token${NC}"
            echo $GITHUB_TOKEN | docker login $REGISTRY -u $GITHUB_USERNAME --password-stdin
        else
            echo -e "${RED}❌ 环境变量 GITHUB_TOKEN 未设置！${NC}"
            echo ""
            echo -e "${YELLOW}请先设置环境变量：${NC}"
            echo "export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxx"
            echo ""
            echo "或者直接运行："
            echo "export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxx && $0"
            exit 1
        fi
        ;;
    2)
        TOKEN_FILE="$HOME/.github_token"
        if [ -f "$TOKEN_FILE" ]; then
            echo -e "${GREEN}✅ 从文件 $TOKEN_FILE 读取Token${NC}"
            cat $TOKEN_FILE | docker login $REGISTRY -u $GITHUB_USERNAME --password-stdin
        else
            echo -e "${YELLOW}💡 将创建Token文件 $TOKEN_FILE${NC}"
            echo "请输入您的GitHub Personal Access Token:"
            read -r TOKEN
            if [ -n "$TOKEN" ]; then
                echo "$TOKEN" > $TOKEN_FILE
                chmod 600 $TOKEN_FILE
                echo -e "${GREEN}✅ Token已保存到 $TOKEN_FILE${NC}"
                cat $TOKEN_FILE | docker login $REGISTRY -u $GITHUB_USERNAME --password-stdin
            else
                echo -e "${RED}❌ Token不能为空！${NC}"
                exit 1
            fi
        fi
        ;;
    3)
        echo -e "${YELLOW}📝 请输入您的GitHub Personal Access Token:${NC}"
        echo "（可以直接粘贴，输入完成后按Enter）"
        read -r TOKEN
        if [ -n "$TOKEN" ]; then
            echo $TOKEN | docker login $REGISTRY -u $GITHUB_USERNAME --password-stdin
        else
            echo -e "${RED}❌ Token不能为空！${NC}"
            exit 1
        fi
        ;;
    4)
        echo -e "${BLUE}📋 手动登录命令：${NC}"
        echo ""
        echo "方法1 - 交互式登录："
        echo "docker login $REGISTRY -u $GITHUB_USERNAME"
        echo ""
        echo "方法2 - 使用Token直接登录："
        echo "echo 'YOUR_TOKEN_HERE' | docker login $REGISTRY -u $GITHUB_USERNAME --password-stdin"
        echo ""
        echo "方法3 - 使用环境变量："
        echo "export GITHUB_TOKEN=YOUR_TOKEN_HERE"
        echo "echo \$GITHUB_TOKEN | docker login $REGISTRY -u $GITHUB_USERNAME --password-stdin"
        echo ""
        exit 0
        ;;
    *)
        echo -e "${RED}❌ 无效选择！${NC}"
        exit 1
        ;;
esac

# 检查登录结果
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 登录成功！${NC}"
    echo "现在您可以推送Docker镜像到 $REGISTRY"
    echo ""
    echo "接下来可以运行："
    echo "./push_docker.sh"
else
    echo ""
    echo -e "${RED}❌ 登录失败！${NC}"
    echo ""
    echo -e "${YELLOW}可能的原因：${NC}"
    echo "1. Token格式错误（应该以 ghp_ 开头）"
    echo "2. Token权限不足（需要 write:packages 权限）"
    echo "3. 用户名错误"
    echo "4. 网络连接问题"
    echo ""
    echo -e "${BLUE}💡 调试建议：${NC}"
    echo "1. 检查Token是否正确复制"
    echo "2. 重新生成Token并确保权限正确"
    echo "3. 检查网络连接"
    exit 1
fi
