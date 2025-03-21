import streamlit as st

def main():
    # 初始化session states
    if 'column_index' not in st.session_state:
        st.session_state.column_index = 0
    if 'content_index' not in st.session_state:
        st.session_state.content_index = {0: 0, 1: 0, 2: 0}  # 每列的内容显示进度

    # 注入CSS样式
    st.markdown("""
        <style>
        .gradient-title {
            background: linear-gradient(120deg, #ffbe00 0%, #ff7c00 40%, #dd0000 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 8em;
            font-weight: 1000;
            text-align: center;
            padding: 20px 0;
            margin-bottom: 100px;
        }

        .content-block {
            opacity: 0;
            transform: translateY(20px);
            animation: fadeIn 0.5s ease forwards;
        }
                
        /* 内容淡入动画 */
        .fade-in {
            animation: fadeIn 0.5s ease-in;
        }

        .column-container {
            opacity: 0;
            transform: translateX(-20px);
            animation: slideIn 0.5s ease forwards;
        }

        @keyframes fadeIn {
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes slideIn {
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        /* 列间距和分隔线样式 */
        [data-testid="column"] {
            padding: 0 3.5rem !important;  /* 增加内边距 */
            position: relative;
            margin: 0 1rem !important;     /* 增加外边距 */
        }
        
        /* 分隔线样式 */
        .column-divider {
            position: absolute;
            right: -1rem;  /* 调整分隔线位置 */
            top: 10%;
            height: 80%;
            width: 2px;
            background: linear-gradient(180deg, 
                rgba(255,190,0,0) 0%, 
                rgba(255,124,0,0.3) 50%, 
                rgba(255,190,0,0) 100%);
        }

        /* 标签页样式 */
        button[data-baseweb="tab"] {
            font-size: 1.8rem !important;
            font-weight: 500 !important;
            padding: 0.5rem 2rem !important;
            background: transparent !重要;ortant;
            border: none !important;
            transition: color 0.3s ease !important;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            background: none !important;
            border: none !important;
            transform: none !important;
            box-shadow: none !important;
            color: #ff7c00 !important;
        }

        [data-testid="stTabsContent"] {
            padding: 2rem 0 !important;
            background: none !important;
            border: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # 标题部分
    st.markdown('<h1 class="gradient-title">什么是大语言模型LLM？</h1>', unsafe_allow_html=True)
    st.markdown("")

    # 创建标签页
    tab1, tab2, tab3 = st.tabs(["你用过Deepseek吗？", "大语言模型因何得名？", "词元是什么？"])

    # 第一个标签页内容
    with tab1:
        col_tab1 = st.columns([0.6, 0.4])
        with col_tab1[0]:
            st.markdown("""
                <div class="fade_in">
                    <h3>你用过Deepseek吗？</h3>
                </div>
            """, unsafe_allow_html=True)
            
            st.image("./images/DeepSeek_logo.png", width=400)
            st.link_button(url="https://deepseek.com", label="前往Deepseek👉")
            st.divider()

            st.markdown("""
                <div class="fade_in">
                    <h3>你用Deepseek帮你做什么？</h3>
                </div>
            """, unsafe_allow_html=True)
            st.divider()

            st.markdown("""
                <div class="fade_in">
                    <h3>你还用过类似的AI聊天工具吗？</h3>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("")
            
            # 修复列创建语法
            sub_col = st.columns([0.25, 0.125, 0.25, 0.125, 0.25])  # 使用括号而不是方括号
            with sub_col[0]:
                st.image("./images/grok.png")
            with sub_col[2]:
                st.image("./images/gpt.png")
            with sub_col[4]:
                st.image("./images/claude.png")

    # 第二个标签页内容
    with tab2:

        col_tab2 = st.columns([0.7, 0.3])
        with col_tab2[0]:
            st.markdown("""
            <div style='text-align: center; color: #ff7c00; font-size: 2em; margin: 0 0 30px 0; font-weight: 1000'>
                大模型的发展
            </div>
        """, unsafe_allow_html=True)

            import matplotlib.pyplot as plt
            import numpy as np
            
            # 设置中文字体
            plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
            plt.rcParams['axes.unicode_minus'] = False

            # 更新数据
            models = ["ChatGPT\n(1750亿)", "GPT-4\n(2000亿)", "Claude 3 Sonnet\n(1750亿)", 
                    "LLaMA 2\n(700亿)", "Gemini\n(7500亿)", "DeepSeek-V3\n(6710亿)"]
            x = [2022, 2023, 2023, 2023, 2023, 2024]  # 年份
            y = [1, 0.6, 1.0, 1.4, 1.8, 1.2]  # 垂直位置
            sizes = [1750, 2000, 1750, 700, 7500, 6710]  # 参数规模（亿）
            
            # 创建图表
            fig, ax = plt.subplots(figsize=(15, 8))
            
            # 设置透明背景
            fig.patch.set_alpha(0.0)
            ax.patch.set_alpha(0.0)
            
            # 绘制散点图，参数规模夸大显示
            sizes_scaled = [s ** 1.15 for s in sizes]  # 调整指数以获得更好的视觉效果
            scatter = ax.scatter(x, y, s=sizes_scaled, 
                            c=['#FF9999', '#66B2FF', '#99FF99', 
                                '#FFCC99', '#FF99CC', '#99CCFF'],  # 修正颜色数组长度
                            alpha=0.6)
            
            # 添加标签，直接在圆形中心显示
            for i, (model, year, y_pos) in enumerate(zip(models, x, y)):
                ax.annotate(
                    model, 
                    (year, y_pos),
                    xytext=(0, 0),  # 不设置偏移
                    textcoords="offset points",
                    ha='center',
                    va='center',
                    fontsize=12,
                    color='white',
                    bbox=None  # 移除背景框
                )
            
            # 设置坐标轴
            ax.set_ylim(0, 2.5)
            ax.set_xlim(2021.5, 2024.5)
            ax.set_xticks([2022, 2023, 2024])
            ax.set_xticklabels(['2022年', '2023年', '2024年'], fontsize=14, color='gray')
            
            # 隐藏y轴但保留框架
            ax.yaxis.set_visible(False)
            
            # 设置标题，使用灰色以适应暗色主题
            # plt.title("大语言模型参数规模对比", fontsize=16, pad=20, color='gray')
            
            # 添加半透明网格线
            ax.grid(True, axis='x', linestyle='--', alpha=0.4, color='gray')
            
            # 设置轴线颜色为灰色
            ax.spines['bottom'].set_color('gray')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)
            
            plt.tight_layout()
            st.pyplot(fig)

        with col_tab2[1]:
            st.markdown("""
            <div style='text-align: center; color: #ff7c00; font-size: 2em; margin: 0 0 30px 0; font-weight: 1000'>
                与Deepseek对比
            </div>
            """, unsafe_allow_html=True) 
            st.markdown("""- 「新华字典」：收录13000字/总计45万字
                        """)
            st.markdown("""- 人脑：860亿神经元，每个神经元有1000个突触
                        """)
            st.divider()
            st.markdown("""Deepseek-V3：
                        """)
            st.markdown("""- 约等于40万本「新华字典」
                        """)
            st.markdown("""- 神经元个数计算:约8个；突触数量计算:1/128
                        """)
            st.markdown("""- 仍未超过人脑的复杂度，人脑依然比LLM复杂
                        """)
            st.divider()
            st.markdown("""
            <div style='text-align: center; color: #ff8c00; font-size: 2em; margin: 0 0 30px 0; font-weight: 1000'>
                大 = 参数多
            </div>
            """, unsafe_allow_html=True) 


            



    # 第三个标签页内容
    with tab3:
        st.markdown("""
            <div style='text-align: center; color: #ff7c00; font-size: 2em; margin: 0 0 30px 0; font-weight: 1000'>
                大语言模型因何得名？
            </div>
        """, unsafe_allow_html=True)


        
 

    # 不再需要column_index和重置按钮
    if 'column_index' in st.session_state:
        del st.session_state.column_index

if __name__ == "__main__":
    main()