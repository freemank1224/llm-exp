import streamlit as st
import json
from score_manager import init_score_state, update_score, get_score_status

def main():
    # 初始化分数状态
    init_score_state(st)

    # 注入CSS样式
    st.markdown("""
        <style>
        .gradient-title {
            background: linear-gradient(120deg, #ffbe00 0%, #ff7c00 40%, #dd0000 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 6em;  /* 调整为与原理图解页面一致 */
            font-weight: 1000;
            text-align: center;
            padding: 20px 0;
            margin-bottom: 30px;
        }
        .tab-content {
            padding: 20px;
            border-radius: 5px;
            min-height: 200px;
        }

        /* 标签样式 */
        button[data-baseweb="tab"] {
            font-size: 1.8rem !important;
            font-weight: 500 !important;
            padding: 0.5rem 2rem !important;
            background: transparent !important;
            border: none !important;
            transition: color 0.3s ease !important;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            background: none !important;
            border: none !important;
            transform: none !important;
            box-shadow: none !important;
            color: #00ffbb !important;
        }

        [data-testid="stTabsContent"] {
            padding: 2rem 0 !important;
            background: none !important;
            border: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # 修改标题和副标题样式以匹配原理图解页面
    st.markdown('<h1 class="gradient-title">谢谢观看！</h1>', unsafe_allow_html=True)
    # st.markdown('<p style="text-align: center; font-size: 1.5em; color: #666;">你可以通过本页的问题，检查一下自己是否理解了LLM的原理</p>', unsafe_allow_html=True)

    # 创建标签页
    tab0, tab1, tab2, tab3 = st.tabs(["🎆更多有趣的内容", "📝 练习题", "📊 成绩统计", "🎯 学习目标"])

    with tab0:
        st.markdown("<h2 class='gradient-title'>💡知识在于分享，本项目已在Github上开源💡</h2>", unsafe_allow_html=True)  # 添加小标题
        st.markdown('''
            <a href="https://github.com/freemank1224/llm-exp/tree/presentation" target="_blank" style="
                display: inline-block;
                padding: 10px 20px;
                background: linear-gradient(120deg, #ffbe00 0%, #ff7c00 40%, #dd0000 100%);
                color: white;
                text-decoration: none;
                border-radius: 5px;
                font-size: 1.2em;
                text-align: center;
                margin: 20px auto;
                display: block;
                width: fit-content;">
                访问本项目的 Github 仓库
            </a>
        ''', unsafe_allow_html=True)
        sub_l, sub_m, sub_r = st.columns([0.3, 0.4, 0.3])
        with sub_l:
            st.markdown("")
        with sub_m:
            st.markdown("""
                <div style="
                margin: 20px auto;
                padding: 20px;
                background-color: rgba(255, 235, 59, 0.1);
                border: 2px solid #FFD700;
                border-radius: 10px;
                ">
                <p style="margin-bottom: 0; font-size: 1.2em; color: #FFF;">
                本项目支持基于英伟达GPU/CPU/MacOS三种环境下的本机部署和运行，但为了保证演示性能，建议在GPU或MacOS上运行。
                </p>
                </div>
            """, unsafe_allow_html=True)  
            st.divider()

        with sub_r:
            st.markdown("") 

        st.markdown("<h2 class='gradient-title'>💡也欢迎关注我的公众号：AI4EDU新视野💡</h2>", unsafe_allow_html=True)  # 添加小标题 
        st.markdown("")
        low_l, low_m, low_r = st.columns([0.25, 0.5, 0.25])
        with low_l:
            st.markdown("")
        with low_m:
            mlow_l, _, mlow_r = st.columns([0.25, 0.05, 0.7])
            with mlow_l:
                st.image("./images/QR_code.jpg")
            with mlow_r:
                st.markdown("""
                    <div style="
                    margin: 0px auto;
                    padding: 20px;
                    background-color: rgba(255, 235, 59, 0.1);
                    border: 2px solid #999;
                    border-radius: 0px;
                    ">
                    <p style="margin-bottom: 0; font-size: 1.2em; color: #FFF;">
                    ✅ 为教育从业者提供最贴近需求的AI教育内容
                    </p>
                    <p style="margin-bottom: 0; font-size: 1.2em; color: #FFF;">
                    ✅ 聚焦教育领域的创业者，体验全新的AI4EDU产品
                    </p>
                    <p style="margin-bottom: 0; font-size: 1.2em; color: #FFF;">
                    ✅ 教育与AI交叉领域内，有志于变革传统教育范式的的伙伴
                    </p>
                    </div>
                """, unsafe_allow_html=True)
        with low_r:
            st.markdown("")
            


    
    
    with tab1:
        st.subheader("理论知识测试")  # 添加小标题
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        if "score" not in st.session_state:
            st.session_state.score = 0
            st.session_state.answers = {}
        
        questions = [
            {
                "question": "语言模型预测下一个词时主要依据什么？",
                "options": [
                    "上下文信息",
                    "随机猜测",
                    "固定规则",
                    "人工设定"
                ],
                "correct": 0
            },
            {
                "question": "temperature参数的作用是什么？",
                "options": [
                    "控制模型的创造性",
                    "控制运行速度",
                    "控制输出长度",
                    "控制模型大小"
                ],
                "correct": 0
            }
        ]
        
        for i, q in enumerate(questions):
            st.subheader(f"问题 {i+1}")
            st.write(q["question"])
            answer = st.radio("选择答案:", q["options"], key=f"q_{i}")
            
            if st.button("提交", key=f"submit_{i}"):
                if q["options"].index(answer) == q["correct"]:
                    st.success("✅ 回答正确！")
                    update_score(st, "实践评估", 1)
                else:
                    st.error("❌ 回答错误。")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.subheader("学习进度追踪")  # 添加小标题
        score_status = get_score_status(st)
        
        # 显示总体进度，添加除零保护
        progress = (score_status['total'] / score_status['max']) if score_status['max'] > 0 else 0
        st.progress(progress)
        st.metric("总得分", f"{score_status['total']}/{score_status['max']}")
        
        # 显示各部分得分
        st.markdown("### 各章节得分")
        for section, data in score_status['sections'].items():
            if data['max'] > 0:  # 只显示有分值的章节
                st.metric(section, f"{data['score']}/{data['max']}")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.subheader("本章节目标")  # 添加小标题
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        st.markdown("""
        ### 本章节学习目标
        1. 理解语言模型的基本原理
        2. 掌握模型参数的作用
        3. 能够运用所学知识解决实际问题
        """)
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
