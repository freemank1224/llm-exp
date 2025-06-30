import streamlit as st
from score_manager import init_score_state, update_score, get_score_status, reset_section_score

def main():
    # 初始化session states
    if 'column_index' not in st.session_state:
        st.session_state.column_index = 0
    if 'content_index' not in st.session_state:
        st.session_state.content_index = {0: 0, 1: 0, 2: 0}  # 每列的内容显示进度
    if 'get_next_content' not in st.session_state:
        st.session_state.get_next_content = 0

    # 初始化分数状态
    init_score_state(st)

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
            animation: titleFadeIn 0.8s ease forwards, gradientFlow 5s linear infinite;
        }
                
        .large-text {
            font-size: 1.5em;
            font-weight: 400;
            text-align: left;
            padding: 10px 0px;
            margin-bottom: 20px;
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
                
        /* 修改：背景单向流动动画 */
        @keyframes gradientFlow {
            0% { background-position: 100% 50%; }
            100% { background-position: -100% 50%; }
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
    st.markdown('<h1 class="gradient-title">什么是「大语言模型」？</h1>', unsafe_allow_html=True)
    st.markdown("")

    # 创建标签页
    tab1, tab2, tab3 = st.tabs(["你用过「大语言模型吗」", "「语言模型」是什么", "为什么说它「大」"])

    # 第一个标签页内容
    with tab1:
        col_tab1 = st.columns([0.5, 0.05, 0.45])
        with col_tab1[0]:
            st.markdown("""
                <div class="fade_in">
                    <h3>你知道Deepseek吗？</h3>
                </div>
            """, unsafe_allow_html=True)

            subcol_l, subcol_r = st.columns([0.7, 0.3])
            with subcol_l:            
                st.image("./images/DeepSeek_logo.png", width=350)                
            with subcol_r:
                st.markdown("")
                
                st.link_button(url="https://deepseek.com", label="前往Deepseek👉", type="secondary")    

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
            # 排列LLM图标
            sub_col = st.columns([0.2, 0.2, 0.2, 0.2, 0.2])  # 使用括号而不是方括号
            with sub_col[0]:
                st.image("./images/grok.png")
            with sub_col[2]:
                st.image("./images/gpt.png")
            with sub_col[4]:
                st.image("./images/claude.png")

            st.divider()

            if st.button("揭秘👉", type="primary"):
                st.session_state.get_next_content = 1
                st.rerun()
        
        with col_tab1[2]:
            if st.session_state.get_next_content != 0:                
                st.markdown('')
                st.markdown('<h2 class="gradient-title">它们是「大语言模型」!</h2>', unsafe_allow_html=True)
                st.markdown('<h2 class="gradient-title">Large Language Model (LLM)</h2>', unsafe_allow_html=True)
                st.divider()

                # 创建单选题
                st.subheader("应该如何读它？")

                # 初始化答题状态
                if 'quiz_1_answered' not in st.session_state:
                    st.session_state.quiz_1_answered = False
                if 'show_answer_feedback' not in st.session_state:
                    st.session_state.show_answer_feedback = False

                option_selected = st.radio(
                    "",
                    ["A. 「大语言」+「模型」", "B. 「大」+「语言模型」"],
                    key="quiz_1"
                )

                btn_l, btn_r = st.columns([0.5, 0.5])
                with btn_l:
                # 添加提交按钮
                    if st.button("提交答案", key="submit_quiz_1", type="primary"):
                        st.session_state.show_answer_feedback = True
                        if not st.session_state.quiz_1_answered:  # 只有第一次回答才计分
                            if option_selected == "B. 「大」+「语言模型」":
                                update_score(st, "问题引入", 1)  # 更新分数
                            st.session_state.quiz_1_answered = True

                    # 显示答案反馈
                    if st.session_state.show_answer_feedback:
                        if option_selected == "B. 「大」+「语言模型」":
                            st.success("✅ 回答正确！")
                        else:
                            st.error("❌ 回答错误。正确答案是：「大」+「语言模型」")

                    # 显示本节得分
                    score_status = get_score_status(st)
                    st.sidebar.markdown(f"### 本节得分: {score_status['sections']['问题引入']['score']}/{score_status['sections']['问题引入']['max']}")

                with btn_r:
                    # 添加重置按钮
                    if st.button("重新作答", key="reset_quiz_1"):
                        st.session_state.quiz_1_answered = False
                        st.session_state.show_answer_feedback = False
                        reset_section_score(st, "问题引入")  # 重置本节分数
                        st.rerun()

                st.divider()

                if st.session_state.quiz_1_answered:
                    st.subheader("❓「大」：指的是什么？")
                    st.subheader("❓「语言模型」是什么？")

    with tab2: 
        tab2_l, _, tab2_r = st.columns([0.5, 0.05, 0.45])
        with tab2_l:
            st.markdown("")         
            st.markdown("""
            <h2 class='gradient-title'>
                🗣️ 用人类语言和人交流的一种程序
            </h2>
        """, unsafe_allow_html=True)
            
            st.divider()
            
            st.markdown("<div class='large-text'>💡「语言」就是我们每天与人交流所用的东西，我们听人讲话、和别人讲话，平时写作业都要使用语言</div>", unsafe_allow_html=True)
            st.markdown("<div class='large-text'>🤖「模型」就是一段AI程序，它的功能就是接收「语言」，并用「语言」回复。</div>", unsafe_allow_html=True)
            st.markdown("<div class='large-text'>🤖 不同国家说不同的语言，现在的「大语言模型」往往懂得不止一门语言，是一个「语言专家」。</div>", unsafe_allow_html=True)

        with tab2_r:
            st.markdown("")
            st.image("./images/LLM.png", caption="图像由AI生成")


    with tab3:
        col_tab2 = st.columns([0.6, 0.05, 0.35])
        with col_tab2[0]:
            st.markdown("""
            <h3 class='gradient-title'>
                「大语言模型」的规模对比
            </h3>
        """, unsafe_allow_html=True)

            import matplotlib.pyplot as plt
            import numpy as np
            
            # 设置中文字体
            # plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
            plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'sans-serif']
            plt.rcParams['axes.unicode_minus'] = False

            # 更新数据
            models = ["ChatGPT\n(1750亿)", "GPT-4\n(2000亿)", "Claude 3 Sonnet\n(1750亿)", 
                    "LLaMA 2\n(700亿)", "DeepSeek-V3\n(6710亿)"]
            x = [2022, 2023, 2023, 2023, 2024]  # 年份
            y = [1, 0.6, 1.0, 1.4, 1.2]  # 垂直位置
            sizes = [1750, 2000, 1750, 700, 6710]  # 参数规模（亿）
            
            # 创建图表
            fig, ax = plt.subplots(figsize=(15, 8))
            
            # 设置透明背景
            fig.patch.set_alpha(0.0)
            ax.patch.set_alpha(0.0)
            
            # 绘制散点图，参数规模夸大显示
            sizes_scaled = [s ** 1.35 for s in sizes]  # 调整指数以获得更好的视觉效果
            scatter = ax.scatter(x, y, s=sizes_scaled, 
                            c=['#FF9999', '#66B2FF', '#99FF99', 
                                '#FFCC99', '#99CCFF'],  # 修正颜色数组长度
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
                    fontsize=15,
                    color='white',
                    bbox=None  # 移除背景框
                )
            
            # 设置坐标轴
            ax.set_ylim(0, 2.5)
            ax.set_xlim(2021.5, 2024.8)  # 缩小横轴范围，使年份更紧凑
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
            st.markdown("")
            st.markdown("""
            <div style='text-align: center; color: #ff8c00; font-size: 2em; margin: 0 0 30px 0; font-weight: 1000'>
                ⚠️ 「大」的意思是参数非常多！
            </div>
            """, unsafe_allow_html=True)

        with col_tab2[2]:
            st.markdown("""
            <h3 class='gradient-title'>
                比比看Deepseek有多「大」？
            </h3>
            """, unsafe_allow_html=True) 
            st.divider()
            st.markdown("""<div class='large-text'>📚「新华字典」：收录13000字/总计45万字</div>""", unsafe_allow_html=True)
            st.markdown("""<div class='large-text'>🧠 人脑：860亿神经元，每个神经元有1000个突触""", unsafe_allow_html=True)
            st.divider()

            st.markdown("<div class='large-text'>❗️约等于150万本「新华字典」，能铺满5个操场</div>", unsafe_allow_html=True)
            st.markdown("<div class='large-text'>❔仍未超过人脑的复杂度，人脑依然比它复杂</div>", unsafe_allow_html=True)
            st.divider()

            st.markdown("⚠️ 2025年又涌现了几个非常厉害的LLM，但是它们并没有公布参数，但是从它们训练所需要的硬件来看，比Deepseek要大很多！")

    # 第三个标签页内容
    # with tab3:
    #     st.markdown("""
    #         <div style='text-align: center; color: #ff7c00; font-size: 2em; margin: 0 0 30px 0; font-weight: 1000'>
    #             大语言模型因何得名？
    #         </div>
    #     """, unsafe_allow_html=True)

    # 不再需要column_index和重置按钮
    if 'column_index' in st.session_state:
        del st.session_state.column_index

if __name__ == "__main__":
    main()