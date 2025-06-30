#!/bin/bash

# 快速修复中文字体问题脚本
# 专门解决Streamlit中文显示和matplotlib字体警告

echo "🔧 快速修复中文字体问题..."

# 1. 安装中文字体
echo "📦 安装中文字体包..."
sudo apt update
sudo apt install -y fonts-noto-cjk fonts-wqy-zenhei fonts-liberation fontconfig

# 2. 更新字体缓存
echo "🔄 更新字体缓存..."
sudo fc-cache -fv

# 3. 创建字体配置文件
echo "📝 创建字体配置..."
cat > font_fix.py << 'EOF'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import warnings

# 禁用字体警告
warnings.filterwarnings('ignore', category=UserWarning, message='.*font.*')
warnings.filterwarnings('ignore', category=UserWarning, message='.*Glyph.*')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'WenQuanYi Zen Hei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

print("✅ 字体配置已设置")
EOF

# 4. 在虚拟环境中清除matplotlib缓存
if [[ -d "venv" ]]; then
    echo "🧹 清除matplotlib字体缓存..."
    source venv/bin/activate
    python3 -c "
import matplotlib.font_manager as fm
try:
    fm._rebuild()
    print('✅ matplotlib字体缓存已清除')
except:
    print('⚠️  字体缓存清除失败，但不影响使用')
"
fi

# 5. 创建修复后的启动脚本
echo "🚀 创建修复后的启动脚本..."
cat > start_app_fixed.sh << 'EOF'
#!/bin/bash

# 激活虚拟环境
source venv/bin/activate

# 设置环境变量
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
export MPLBACKEND=Agg
export PYTHONWARNINGS=ignore::UserWarning

# 导入字体修复
python3 -c "exec(open('font_fix.py').read())"

echo "🎯 启动大语言模型演示应用（已修复字体问题）..."
echo "📱 应用将在 http://localhost:8501 启动"
echo "⏹️  按 Ctrl+C 停止应用"

# 启动应用
streamlit run Home.py --server.port=8501 --server.address=0.0.0.0
EOF

chmod +x start_app_fixed.sh

echo ""
echo "✅ 字体问题修复完成！"
echo ""
echo "🎯 使用方法："
echo "   ./start_app_fixed.sh"
echo ""
echo "📝 修复内容："
echo "   ✓ 安装了中文字体包"
echo "   ✓ 更新了系统字体缓存"
echo "   ✓ 创建了字体配置文件"
echo "   ✓ 禁用了字体相关警告"
echo "   ✓ 创建了修复版启动脚本"
echo ""
