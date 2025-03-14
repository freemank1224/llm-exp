import streamlit as st
import time

def main():
    # 初始化 session state
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0

    # 注入CSS样式
    st.markdown("""
        <style>
        .gradient-title {
            background: linear-gradient(140deg, #00ffbb 0%, #3d9dff 50%, #7f2aff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 6em;
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
            color: #FF4B4B !important;
        }

        [data-testid="stTabsContent"] {
            padding: 2rem 0 !important;
            background: none !important;
            border: none !important;
        }

        /* 打字机动画容器 */
        .typewriter-container {
            background: rgba(0, 0, 0, 0.1);
            padding: 2rem;
            border-radius: 10px;
            margin: 20px 0;
        }
        
        /* 打字机文本样式 */
        .typewriter-text {
            font-family: monospace;
            font-size: 1.5em;
            color: #00ffbb;
            position: relative;
            white-space: pre;
            display: inline-block;
        }
        
        /* 光标样式 */
        .typewriter-text::after {
            content: '';
            position: absolute;
            right: -4px;
            top: 0;
            height: 100%;
            width: 3px;
            background: #00ffbb;
            animation: blink-caret 1s step-end infinite;
        }

        /* 字符显示动画 */
        .typewriter-text {
            opacity: 0;
        }
        
        .typewriter-text.start {
            opacity: 1;
            animation: type 3.5s steps(40, end);
        }
        
        /* 光标闪烁动画 */
        @keyframes blink-caret {
            from, to { opacity: 1; }
            50% { opacity: 0; }
        }
        
        /* 文本显示动画 */
        @keyframes type {
            from { clip-path: inset(0 100% 0 0); }
            to { clip-path: inset(0 0 0 0); }
        }

        .demo-text {
            margin: 1rem 0;
            position: relative;
        }

        /* 循环动画容器 */
        .loop-container {
            animation: fadeInOut 7s infinite;
            animation-delay: calc(var(--delay) * 1s);
        }

        @keyframes fadeInOut {
            0% { opacity: 0; }
            5% { opacity: 1; }
            95% { opacity: 1; }
            100% { opacity: 0; }
        }

        /* 添加下一步按钮样式 */
        .next-button {
            position: fixed;
            bottom: 40px;
            right: 40px;
            padding: 15px 30px;
            background: rgba(0, 255, 187, 0.1);
            border: 1px solid #00ffbb;
            border-radius: 8px;
            color: #00ffbb;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .next-button:hover {
            background: rgba(0, 255, 187, 0.2);
            transform: translateY(-2px);
        }

        /* 内容淡入动画 */
        .fade-in {
            animation: fadeIn 0.5s ease-in;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        </style>
    """, unsafe_allow_html=True)

    #st.title("语言模型原理图解")
    st.markdown('<h1 class="gradient-title">大语言模型是怎么工作的？它为什么能一直吐字呢？</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.5em; color: #666;">构思一个场景，然后一个字一个字的写在本子上</p>', unsafe_allow_html=True)
    
    tabs = st.tabs(["观察现象", "你如何写作文", "大语言模型这样工作"])
    
    with tabs[0]:
        # 第一步内容
        if st.session_state.current_step >= 0:
            st.markdown("""
                <div class="fade-in">
                <h2>1. 你们与Deepseek对过话吗？它是如何回答你的？</h2>
                </div>
            """, unsafe_allow_html=True)
            
            with st.expander("查看动态演示"):
                demo_texts = [
                    "人工智能将改变我们的生活的方方面面"
                ]
                
                for i, text in enumerate(demo_texts):
                    st.markdown(f"""
                        <div class="typewriter-container">
                            <div class="loop-container" style="--delay: {i * 10}">
                                <div class="demo-text">
                                    <span class="typewriter-text start">{text}</span>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("""
                **它是一个字一个字显示出来的！**
                """)

        # 第二步内容
        if st.session_state.current_step >= 1:
            st.markdown("""
                <div class="fade-in">
                <h2>2. 那么，你认为它给你的答案，是一个字一个字思考的呢，还是一次性全部想好，然后逐个字吐出来的呢？</h2>
                </div>
            """, unsafe_allow_html=True)

        # 下一步按钮
        if st.session_state.current_step < 1:  # 最多显示两个主题
            if st.button("下一步 ▶", key="next_button"):
                st.session_state.current_step += 1
                st.rerun()
        
    with tabs[1]:
        st.markdown("""
        ## Transformer架构
        Transformer是现代语言模型的基础架构，它包含：
        - 多头注意力层
        - 前馈神经网络
        - 层归一化
        """)
        
    with tabs[2]:
        st.markdown("""
        ## 训练过程
        语言模型的训练过程包括：
        1. 数据预处理
        2. Token化
        3. 模型优化
        """)

if __name__ == "__main__":
    main()
