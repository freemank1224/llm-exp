import streamlit as st
import json

def main():
    # 注入CSS样式
    st.markdown("""
        <style>
        .gradient-title {
            background: linear-gradient(140deg, #00ffbb 0%, #3d9dff 50%, #7f2aff 100%);
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
    st.markdown('<h1 class="gradient-title">测一测你的学习成果</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.5em; color: #666;">通过这些练习，检验你对语言模型的理解程度</p>', unsafe_allow_html=True)

    # 创建标签页
    tab1, tab2, tab3 = st.tabs(["📝 练习题", "📊 成绩统计", "🎯 学习目标"])

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
                    st.session_state.score += 1
                else:
                    st.error("❌ 回答错误。")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.subheader("学习进度追踪")  # 添加小标题
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        st.markdown("### 学习进度")
        st.progress(st.session_state.score / 2)  # 假设总分为2
        st.metric("当前得分", f"{st.session_state.score}/2")
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
