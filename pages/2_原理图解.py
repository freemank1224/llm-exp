import streamlit as st
import time, os
from score_manager import init_score_state, update_score, get_score_status

def main():
    # 初始化 session states
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0
    if 'block_index' not in st.session_state:
        st.session_state.block_index = 0
    if 'token_index' not in st.session_state:
        st.session_state.token_index = 0
    if 'completed_tokens' not in st.session_state:
        st.session_state.completed_tokens = []
    if 'input_key' not in st.session_state:
        st.session_state.input_key = 0  # 用于重置输入框

    # 初始化分数状态
    init_score_state(st)

    # 注入CSS样式
    st.markdown("""
        <style>
        .gradient-title {
            background: linear-gradient(120deg, #ffbe00 0%, #ff7c00 40%, #dd0000 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 7em;
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
            color: #ff4b4b;
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
            background: #ff4b4b;
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

        /* 文字块动画 */
        .text-block {
            opacity: 0;
            transform: translateY(20px);
            transition: all 0.5s ease;
        }

        .text-block.visible {
            opacity: 1;
            transform: translateY(0);
        }

        /* 图片样式 */
        .gradient-border-image {
            border: 4px solid;
            border-image: linear-gradient(120deg, #ffbe00, #ff7c00, #dd0000) 1;
            opacity: 0;
            transform: scale(0.95);
            transition: all 0.5s ease;
            max-width: 100%;
            height: auto;
        }

        .gradient-border-image.visible {
            opacity: 1;
            transform: scale(1);
        }

        /* 点击提示 */
        .click-hint {
            position: fixed;
            bottom: 20px;
            right: 20px;
            font-size: 1.2rem;
            color: #00ffbb;
            background: rgba(0, 0, 0, 0.5);
            padding: 10px 20px;
            border-radius: 5px;
        }

        /* 添加新的渐变文本样式 */
        .gradient-text {
            font-size: 2.5em;  /* 统一字体大小 */
            background: linear-gradient(120deg, #ffbe00 0%, #ff7c00 40%, #dd0000 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: bold;
            display: inline;
        }
        
        /* 修改词元样式 */
        .token-normal {
            font-size: 2.5em;  /* 统一字体大小 */
            font-weight: bold;
            color: #666;
            display: inline;
        }
        
        /* 基础句子样式 */
        .base-text {
            font-size: 2.5em;  /* 调整为和词元一致的大小 */
            font-weight: bold;
            display: inline;
        }
                
        /* 词元选项容器 */
        .token-options {
            font-size: 1.5em;
            font-weight: bold;
            display: flex;
            align-items: center;
            padding: 5px 25px;  /* 增加内边距使色块更大 */
            border-radius: 5px;  /* 增加圆角 */
            margin: 2px 0;      /* 增加外边距 */
            transition: all 0.3s ease;  /* 添加过渡效果 */
        }
        
        .token-options:hover {
            transform: scale(1.02);  /* 添加悬停效果 */
        }
        
        /* 增大句子显示 */
        .large-sentence {
            line-height: 1.5;
            padding: 30px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            margin: 30px 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <script>
            function handleKeyPress(event) {
                if (event.key === 'Enter' || event.type === 'click') {
                    const blocks = document.querySelectorAll('.text-block:not(.visible), .gradient-border-image:not(.visible)');
                    if (blocks.length > 0) {
                        blocks[0].classList.add('visible');
                    }
                }
            }

            document.addEventListener('keypress', handleKeyPress);
            document.addEventListener('click', handleKeyPress);
        </script>
    """, unsafe_allow_html=True)

    #st.title("语言模型原理图解")
    st.markdown('<h1 class="gradient-title">「大语言模型」是怎么工作的？</h1>', unsafe_allow_html=True)
    st.markdown("")
    # st.markdown('<p style="text-align: center; font-size: 1.5em; color: #666;">构思一个场景，然后一个字一个字的写在本子上</p>', unsafe_allow_html=True)    
    tabs = st.tabs(["你是怎么写作文的", "「写话」的技巧", "大语言模型如何「写作文」", "什么是「词元」"])
    
    # 基础句子
    base_sentence = "今天星期六，天气晴朗，我和" 


    with tabs[1]:
        top_l, top_r = st.columns([0.8, 0.2])
        with top_l:
            st.markdown("""
                    <div class="fade-in">
                    <h2>老师教我们怎么「写话」？</h2>
                    </div>
                """, unsafe_allow_html=True)
        with top_r:
            if st.button(
                "点此重置",
                use_container_width=False,
                type="secondary"
            ):
                st.session_state.completed_tokens = []
                st.session_state.token_index = 0
                st.session_state.token_options = []  # 改为空列表，将动态扩展
                st.session_state.input_key = 0
                st.rerun()
        
        # 显示当前句子状态
        current_text = f'<span class="base-text">{base_sentence}</span>'
        for i, token in enumerate(st.session_state.completed_tokens):
            if i == len(st.session_state.completed_tokens) - 1:
                current_text += f'<span class="gradient-text">{token}</span> '
            else:
                current_text += f'<span class="token-normal">{token}</span> '
        
        st.markdown(f'<div class="large-sentence">{current_text}_________</div>', unsafe_allow_html=True)

        col_l, _, col_r = st.columns([0.55, 0.05, 0.4])
        with col_l:
            st.markdown(f"### 第 {st.session_state.token_index + 1} 个词元")
            
            # 初始化或扩展token_options列表
            if 'token_options' not in st.session_state:
                st.session_state.token_options = []
            
            # 确保token_options列表长度足够
            while len(st.session_state.token_options) <= st.session_state.token_index:
                st.session_state.token_options.append([])
            
            # 添加新的备选词元
            new_option = st.text_input(
                "输入新的备选词元:",
                key=f"new_option_{st.session_state.token_index}_{st.session_state.input_key}"
            )
            if st.button("添加", key=f"add_{st.session_state.token_index}", use_container_width=True) and new_option:
                current_options = st.session_state.token_options[st.session_state.token_index]
                if new_option not in current_options:
                    current_options.append(new_option)
                    st.session_state.token_options[st.session_state.token_index] = current_options
                    st.session_state.input_key += 1
                    st.rerun()

        with col_r:
            st.markdown("### 可选词元:")
            
            # 定义配色方案
            colors = [
                "rgba(255, 99, 132, 0.2)",  # 红色
                "rgba(54, 162, 235, 0.2)",   # 蓝色
                "rgba(255, 206, 86, 0.2)",   # 黄色
                "rgba(75, 192, 192, 0.2)",   # 青色
                "rgba(153, 102, 255, 0.2)"   # 紫色
            ]

            st.markdown('<div class="token-options-container">', unsafe_allow_html=True)
            
            for i, option in enumerate(st.session_state.token_options[st.session_state.token_index]):
                color = colors[i % len(colors)]
                col1, col2 = st.columns([0.7, 0.3])
                
                with col1:
                    st.markdown(
                        f'<div class="token-options" style="background-color: {color};">{option}</div>',
                        unsafe_allow_html=True
                    )
                with col2:
                    if st.button(
                        "选择",
                        key=f"option_{st.session_state.token_index}_{i}",
                        use_container_width=True,
                        type="primary"
                    ):
                        st.session_state.completed_tokens.append(option)
                        st.session_state.token_index += 1
                        st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

    with tabs[2]:
        # 第一步内容
        if st.session_state.current_step >= 0:
            st.markdown("""
                <div class="fade-in">
                <h2>1. Deepseek如何回答你的问题？</h2>
                </div>
            """, unsafe_allow_html=True)
            
            with st.expander("查看动态演示"):
                demo_texts = [
                    "今天星期六，天气特别好，"
                ]
                
                for i, text in enumerate(demo_texts):
                    st.markdown(f"""
                        <div class="typewriter-container">
                            <div class="loop-container" style="--delay: {i * 2}">
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
                <h2>2. 你认为它是如何工作的？</h2>
                </div>
            """, unsafe_allow_html=True)

            if not "score" in st.session_state:
                st.session_state.score = 0
                st.session_state.answers = {}

            questions = [
                {
                    "question":"Deepseek这样工作：",
                    "options":[
                        "先把所有的内容生成完，然后一字一词的显示出来",
                        "逐字逐词的生成，生成一个就马上显示出来，然后再生成下一个"
                    ],
                    "correct": 1
                }
            ]

            for i, q in enumerate(questions):
                # st.write(f"问题 {i+1}: {q['question']}")
                # st.radio("选择答案:", q["options"], key=f"q_{i}")
                answer = st.radio("", q["options"], key=f"q_{i}")

                if st.button("提交", key=f"submit_{i}"):
                    if q["options"].index(answer) == q["correct"]:
                        st.success("✅ 回答正确！")
                        update_score(st, "原理图解", 1)  # 更新分数
                    else:
                        st.error("❌ 回答错误。")

        # 显示当前章节得分
        score_status = get_score_status(st)
        st.sidebar.markdown(f"### 本节得分: {score_status['sections']['原理图解']['score']}/{score_status['sections']['原理图解']['max']}")

        # 第三步内容
        if st.session_state.current_step >= 2:
            st.markdown("""
                <div class="fade-in">
                <h2>3. 究竟是逐字，还是逐词生成呢？</h2>
                </div>
            """, unsafe_allow_html=True)

        # 下一步按钮
        if st.session_state.current_step < 2:  # 最多显示两个主题
            if st.button("下一步 ▶", key="next_button"):
                st.session_state.current_step += 1
                st.rerun()
        
    with tabs[0]:
        col_tab = st.columns([0.4, 0.05, 0.55])

        with col_tab[2]:
            blocks = [
                ("写作文的过程", "h1"),
                ("""
                • 根据要求，规划段落（脑海）\n
                • 确定段落中的句子（脑海）\n
                • 逐词逐字填充句子（手+笔）
                """, "list"),
                ("总结：从整体到部分，从段落到句子，最后逐字逐词的填充句子", "h2")
            ]
            
            # 显示到当前block_index的所有内容
            for i, (text, style) in enumerate(blocks):
                if i <= st.session_state.block_index:
                    if style == "h1":
                        st.header(text)
                    elif style == "p":
                        st.write(text)
                    elif style == "list":
                        st.markdown(text)
                    else:
                        st.subheader(text)
        
            # 在第一个内容块显示后显示SVG
            if st.session_state.block_index >= 1:
                st.image('./images/DiaryNew.svg', use_container_width=True, caption="图像来源：由AI生成")

        with col_tab[0]:
            st.image('./images/writingBoy.png', use_container_width=True, caption="图像为AI生成")

        # 添加下一步按钮
        if st.button("下一步", key="next_block"):
            if st.session_state.block_index < len(blocks):
                st.session_state.block_index += 1
                st.rerun()
    
    with tabs[3]:
        st.markdown("""
        ## LLM生成文本的单位是：「词元」
        了解大语言模型如何将文本拆分为词元(Token)
        """)
        
        # 初始化分词状态
        if 'predictor' not in st.session_state:
            from model import LLMPredictor
            st.session_state.predictor = LLMPredictor()
            
        if 'tokenized' not in st.session_state:
            st.session_state.tokenized = False

        # 示例文本
        sample_texts = {
            "中文": "今天天气真不错，我们一起去春游吧！",
            "英文": "The quick brown fox jumps over the lazy dog."
        }

        selected_lang = st.radio("选择语言", ["中文", "英文"], key="token_lang")
        user_text = st.text_input("输入要分析的文本", value=sample_texts[selected_lang])

        # 添加新的 CSS 样式
        st.markdown("""
            <style>
            .token-container {
                margin: 20px 0;
                line-height: 2.5;
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                align-items: center;
            }
            .token-item {
                display: inline-block;
                padding: 4px 8px;
                border-radius: 4px;
                opacity: 0;
                transform: translateY(10px);
            }
            @keyframes tokenAppear {
                to {
                    opacity: 1;w
                    transform: translateY(0);
                }
            }
            </style>
        """, unsafe_allow_html=True)

        if st.button("开始分词分析"):
            try:
                # 获取对应的模型和分词器
                model, tokenizer = st.session_state.predictor._get_model_and_tokenizer(selected_lang)
                
                # 对文本进行编码和解码
                encoded = tokenizer.encode(user_text)
                tokens = [tokenizer.decode([id]).strip() for id in encoded]
                
                # 使用不同的颜色显示tokens
                colors = [
                    'rgba(255, 99, 132, 0.3)',  # 红色
                    'rgba(54, 162, 235, 0.3)',   # 蓝色
                    'rgba(255, 206, 86, 0.3)',   # 黄色
                    'rgba(75, 192, 192, 0.3)',   # 青色
                    'rgba(153, 102, 255, 0.3)',  # 紫色
                ]
                
                # 生成Token展示HTML
                token_html = '<div class="token-container">'
                for i, token in enumerate(tokens):
                    color = colors[i % len(colors)]
                    token_html += f'''
                        <span class="token-item" style="
                            background-color: {color};
                            animation: tokenAppear 0.5s ease forwards;
                            animation-delay: {i * 0.1}s;">
                            {token}
                        </span>'''
                token_html += '</div>'
                
                # st.markdown(token_html, unsafe_allow_html=True)
                
                # 显示分词结果
                st.markdown(token_html, unsafe_allow_html=True)
                
                # 显示统计信息
                st.info(f"文本被分成了 {len(tokens)} 个词元（Token）")
                
                # 显示Token ID信息
                with st.expander("查看Token详细信息"):
                    st.json({
                        "tokens": tokens,
                        "token_ids": encoded
                    })
                
            except Exception as e:
                st.error(f"分词过程出现错误: {str(e)}")

if __name__ == "__main__":
    main()