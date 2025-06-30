"""
带字体修复的应用启动文件
解决Ubuntu服务器中文显示问题
"""

import os
import warnings
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 设置matplotlib后端（在导入其他模块之前）
matplotlib.use('Agg')

# 禁用字体相关警告
warnings.filterwarnings('ignore', category=UserWarning, message='.*font.*')
warnings.filterwarnings('ignore', category=UserWarning, message='.*Glyph.*')
warnings.filterwarnings('ignore', category=UserWarning, message='.*findfont.*')

def setup_chinese_fonts():
    """设置中文字体支持"""
    
    # 中文字体优先级列表
    chinese_fonts = [
        'Noto Sans CJK SC',
        'Noto Sans CJK TC',
        'WenQuanYi Zen Hei', 
        'WenQuanYi Micro Hei',
        'AR PL UKai CN',
        'AR PL UMing CN',
        'SimHei',
        'Microsoft YaHei',
        'DejaVu Sans'
    ]
    
    # 尝试设置字体
    for font_name in chinese_fonts:
        try:
            font_path = fm.findfont(fm.FontProperties(family=font_name))
            if font_path and os.path.exists(font_path):
                plt.rcParams['font.sans-serif'] = [font_name] + plt.rcParams['font.sans-serif']
                plt.rcParams['axes.unicode_minus'] = False
                print(f"已设置字体: {font_name}")
                return font_name
        except:
            continue
    
    # 如果没有找到中文字体，使用默认设置
    plt.rcParams['axes.unicode_minus'] = False
    print("警告: 未找到中文字体，使用默认字体")
    return None

# 设置环境变量
os.environ['MPLBACKEND'] = 'Agg'
os.environ['PYTHONWARNINGS'] = 'ignore::UserWarning'

# 执行字体设置
setup_chinese_fonts()

# 现在导入应用模块
import streamlit as st

# 设置页面配置
st.set_page_config(
    page_title="生成式AI如何回答你的问题",
    page_icon="🎓",
    layout="wide"
)

# 导入并运行主应用
try:
    from Home import main
    if __name__ == "__main__":
        main()
except ImportError:
    # 如果Home模块不存在，直接运行Home.py的内容
    exec(open('Home.py').read())
