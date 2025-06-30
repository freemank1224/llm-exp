#!/bin/bash

# Ubuntu 22.04 部署验证脚本
# 用于验证部署环境和配置的正确性

# set -e  # 注释掉，避免脚本在测试失败时退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 计数器
PASSED=0
FAILED=0

# 测试函数
test_passed() {
    echo -e "${GREEN}[PASS]${NC} $1"
    ((PASSED++))
}

test_failed() {
    echo -e "${RED}[FAIL]${NC} $1"
    ((FAILED++))
}

test_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

test_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# 检查文件存在性
check_files() {
    test_info "检查部署文件..."
    
    local files=(
        "deploy_ubuntu.sh"
        "requirements_lin.txt"
        ".env.ubuntu"
        "Dockerfile.ubuntu"
        "docker-compose.ubuntu.yml"
        "DEPLOY_UBUNTU.md"
        "SYSTEM_REQUIREMENTS.md"
        "README_UBUNTU.md"
        "Home.py"
        "main.py"
        "model.py"
    )
    
    for file in "${files[@]}"; do
        if [[ -f "$file" ]]; then
            test_passed "文件存在: $file"
        else
            test_failed "文件缺失: $file"
        fi
    done
}

# 检查脚本权限
check_permissions() {
    test_info "检查脚本权限..."
    
    if [[ -x "deploy_ubuntu.sh" ]]; then
        test_passed "deploy_ubuntu.sh 有执行权限"
    else
        test_failed "deploy_ubuntu.sh 没有执行权限"
    fi
}

# 检查脚本语法
check_script_syntax() {
    test_info "检查脚本语法..."
    
    if bash -n deploy_ubuntu.sh; then
        test_passed "deploy_ubuntu.sh 语法正确"
    else
        test_failed "deploy_ubuntu.sh 语法错误"
    fi
    
    if [[ -f "start_app.sh" ]]; then
        if bash -n start_app.sh; then
            test_passed "start_app.sh 语法正确"
        else
            test_failed "start_app.sh 语法错误"
        fi
    else
        test_warning "start_app.sh 不存在（将由部署脚本生成）"
    fi
}

# 检查Python依赖文件
check_requirements() {
    test_info "检查Python依赖文件..."
    
    if [[ -f "requirements_lin.txt" ]]; then
        # 检查关键包是否存在
        local key_packages=("torch" "transformers" "streamlit" "numpy" "pandas")
        
        for package in "${key_packages[@]}"; do
            if grep -q "^${package}==" requirements_lin.txt; then
                test_passed "关键包存在: $package"
            else
                test_failed "关键包缺失: $package"
            fi
        done
        
        # 检查是否有重复包
        local duplicates=$(cut -d'=' -f1 requirements_lin.txt | sort | uniq -d)
        if [[ -z "$duplicates" ]]; then
            test_passed "没有重复的包定义"
        else
            test_failed "发现重复的包: $duplicates"
        fi
    else
        test_failed "requirements_lin.txt 文件不存在"
    fi
}

# 检查Docker配置
check_docker_config() {
    test_info "检查Docker配置..."
    
    # 检查Dockerfile语法（简单检查）
    if [[ -f "Dockerfile.ubuntu" ]]; then
        if grep -q "FROM ubuntu:22.04" Dockerfile.ubuntu; then
            test_passed "Dockerfile 使用正确的基础镜像"
        else
            test_failed "Dockerfile 基础镜像不正确"
        fi
        
        if grep -q "EXPOSE 8501" Dockerfile.ubuntu; then
            test_passed "Dockerfile 暴露正确端口"
        else
            test_failed "Dockerfile 端口配置错误"
        fi
    fi
    
    # 检查docker-compose配置
    if [[ -f "docker-compose.ubuntu.yml" ]]; then
        if grep -q "8501:8501" docker-compose.ubuntu.yml; then
            test_passed "Docker Compose 端口映射正确"
        else
            test_failed "Docker Compose 端口映射错误"
        fi
    fi
}

# 检查环境配置
check_env_config() {
    test_info "检查环境配置..."
    
    if [[ -f ".env.ubuntu" ]]; then
        local env_vars=("STREAMLIT_SERVER_PORT" "HF_HOME" "TORCH_HOME")
        
        for var in "${env_vars[@]}"; do
            if grep -q "^${var}=" .env.ubuntu; then
                test_passed "环境变量存在: $var"
            else
                test_failed "环境变量缺失: $var"
            fi
        done
    else
        test_failed ".env.ubuntu 文件不存在"
    fi
}

# 检查文档完整性
check_documentation() {
    test_info "检查文档完整性..."
    
    local docs=("DEPLOY_UBUNTU.md" "SYSTEM_REQUIREMENTS.md" "README_UBUNTU.md")
    
    for doc in "${docs[@]}"; do
        if [[ -f "$doc" ]]; then
            if [[ -s "$doc" ]]; then
                test_passed "文档存在且非空: $doc"
            else
                test_failed "文档为空: $doc"
            fi
        else
            test_failed "文档缺失: $doc"
        fi
    done
}

# 检查系统兼容性（如果在Ubuntu上运行）
check_system_compatibility() {
    test_info "检查系统兼容性..."
    
    if [[ -f /etc/os-release ]]; then
        source /etc/os-release
        
        if [[ "$ID" == "ubuntu" ]]; then
            test_passed "运行在Ubuntu系统上"
            
            if [[ "$VERSION_ID" == "22.04" ]]; then
                test_passed "Ubuntu版本正确: $VERSION_ID"
            else
                test_warning "Ubuntu版本不是22.04: $VERSION_ID"
            fi
        else
            test_warning "不是Ubuntu系统: $ID"
        fi
    else
        test_warning "无法检测系统版本"
    fi
    
    # 检查Python版本
    if command -v python3 &> /dev/null; then
        local python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
        
        if [[ "$python_version" == "3.10" ]]; then
            test_passed "Python版本正确: $python_version"
        else
            test_warning "Python版本不是3.10: $python_version"
        fi
    else
        test_warning "Python3未安装"
    fi
}

# 主函数
main() {
    echo "=========================================="
    echo "Ubuntu 22.04 部署配置验证"
    echo "=========================================="
    echo ""
    
    check_files
    echo ""
    
    check_permissions
    echo ""
    
    check_script_syntax
    echo ""
    
    check_requirements
    echo ""
    
    check_docker_config
    echo ""
    
    check_env_config
    echo ""
    
    check_documentation
    echo ""
    
    check_system_compatibility
    echo ""
    
    # 总结
    echo "=========================================="
    echo "验证结果总结"
    echo "=========================================="
    echo -e "${GREEN}通过测试: $PASSED${NC}"
    echo -e "${RED}失败测试: $FAILED${NC}"
    echo ""
    
    if [[ $FAILED -eq 0 ]]; then
        echo -e "${GREEN}✅ 所有验证通过！部署配置正确。${NC}"
        exit 0
    else
        echo -e "${RED}❌ 发现 $FAILED 个问题，请修复后重新验证。${NC}"
        exit 1
    fi
}

# 执行主函数
main "$@"
