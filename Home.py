import streamlit as st
from datetime import datetime

def main():
    st.set_page_config(
        page_title="生成式AI如何回答你的问题",
        page_icon="🎓",
        layout="wide"
    )

    # 注入自定义CSS，修改动画实现
    st.markdown("""
        <style>
        /* 页面容器样式 */
        .main-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            min-height: 100vh;
            padding: 2rem 0;
            margin-top: -8rem;  /* 整体向上移动 */
        }
        
        /* 标题容器样式 */
        .title-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            flex: 1;
            margin-bottom: 4rem;  /* 增加底部间距 */
        }
        
        /* 标题文本样式，调整上边距 */
        .title-text {
            margin-top: -4rem;  /* 标题向上移动 */
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 9rem;
            font-weight: 1000;
            text-align: center;
            background: linear-gradient(120deg, #ffbe00 0%, #ff7c00 40%, #dd0000 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            opacity: 0;
            transform: translateY(20px);
            animation: titleFadeIn 0.8s ease forwards;
        }
        
        @keyframes titleFadeIn {
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* 副标题样式修改 */
        .subtitle-container {
            opacity: 0;
            animation: fadeIn 0.5s ease forwards 0.8s;
        }
        
        .subtitle-text {
            color: #888;
            font-size: 3em;
            text-align: center;
            font-weight: 300;
            margin-top: 25px;
        }
        
        /* 页脚固定在底部 */
        .footer {
            position: flex;
            bottom: 20px;
            width: 100%;
            text-align: center;
            color: #999;
            font-size: 1.2em;
            left: 0;
            opacity: 0;
            animation: fadeIn 0.5s ease forwards 1s;
        }

        @keyframes fadeIn {
            to {
                opacity: 1;
            }
        }

        /* 添加光标动画效果 */
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0; }
        }
        
        .cursor {
            display: inline-block;
            width: 4px;
            height: 100px;
            background: #ff7c00;
            margin-left: 10px;
            vertical-align: middle;
            animation: blink 1s step-end infinite;
            opacity: 0;
            animation-delay: 0.8s;  /* 与标题出现同步 */
        }
        </style>
    """, unsafe_allow_html=True)

    # 使用新的容器结构渲染页面
    st.markdown("""
        <div class="main-container">
            <div class="title-container">
                <div class="title-text">
                    <div>逐字预测的奥秘</div>
                    <div class="cursor"></div>
                </div>
                <div class="subtitle-container">
                    <div class="subtitle-text">大语言模型是怎么工作的？</div>
                </div>
            </div>
            <div class="footer">
                张国煜「戴森老师」 |  演讲时间：""" + datetime.now().strftime('%Y-%m-%d') + """
            </div>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
