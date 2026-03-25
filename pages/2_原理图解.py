import streamlit as st
import time, os
from pathlib import Path
from urllib.parse import quote
from score_manager import init_score_state, update_score, get_score_status


def render_svg(svg_relative_path: str, caption: str = ""):
    svg_path = Path(__file__).resolve().parents[1] / svg_relative_path
    with open(svg_path, "r", encoding="utf-8") as svg_file:
        svg_content = svg_file.read()

    svg_data_url = f"data:image/svg+xml;utf8,{quote(svg_content)}"
    st.markdown(
        f'<img src="{svg_data_url}" style="width: 100%; height: auto;" />',
        unsafe_allow_html=True,
    )
    if caption:
        st.caption(caption)

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
    if 'caution_flag' not in st.session_state:
        st.session_state.caution_flag = 0   # 用来显示⚠️文字
    if 'image_flag' not in st.session_state:
        st.session_state.image_flag = 0

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
            margin-bottom: 20px;
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
            margin: 10px 0;
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
            font-size: 3em;  /* 修改为3em，与base-text一致 */
            background: linear-gradient(120deg, #ffbe00 0%, #ff7c00 40%, #dd0000 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: bold;
            display: inline;
            margin: 0 10px;
            padding: 5px 10px;
        }
        
        /* 修改词元样式 */
        .token-normal {
            font-size: 3em;  /* 修改为3em，与base-text一致 */
            font-weight: bold;
            color: #666;
            display: inline;
        }
        
        /* 基础句子样式 */
        .base-text {
            font-size: 3em;  /* 保持3em作为基准大小 */
            font-weight: bold;
            display: inline;
        }

        /* 调整大句子容器的样式以容纳更大的文本 */
        .large-sentence {
            line-height: 1.8;  /* 增加行高以适应更大的文本 */
            padding: 40px;     /* 增加内边距 */
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            margin: 40px 0;    /* 增加外边距 */
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .token-container {
            margin: 30px 0;
            line-height: 2;
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            align-items: center;
            background: rgba(255, 255, 255, 0.05);
            padding: 20px;
            border-radius: 10px;
        }
        .token-item {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 8px;
            opacity: 0;
            transform: translateY(20px);
            font-size: 1.8em;
            font-weight: bold;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        @keyframes tokenAppear {
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        /* 词元选项容器 */
        .token-options {
            font-size: 1.6em;  /* 增大到与基础文本一致 */
            font-weight: bold;
            display: flex;
            align-items: center;
            padding: 3px 20px;  /* 增加内边距使色块更大 */
            border-radius: 8px;  /* 稍微增大圆角 */
            margin: 2px 0;     /* 增加选项间距 */
            transition: all 0.3s ease;
            line-height: 1.5;   /* 调整行高 */
        }
        
        /* 调整词元选项容器的样式 */
        .token-options-container {
            padding: 10px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            margin-top: 10px;
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
    base_sentence = "今天星期六，天气很好，我和"


    with tabs[1]:
        top_l, top_r = st.columns([0.8, 0.2])
        with top_l:
            st.markdown("""
                    <div class="fade-in">
                    <h2>如何写出一句话？</h2>
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
                "输入你想到的词:",
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
            st.markdown("### 脑海中的可选词:")
            
            # 定义配色方案
            colors = [
                "rgba(255, 99, 132, 0.2)",  # 红色
                "rgba(54, 162, 235, 0.2)",   # 蓝色
                "rgba(255, 206, 86, 0.2)",   # 黄色
                "rgba(75, 192, 192, 0.2)",   # 青色
                "rgba(153, 102, 255, 0.2)"   # 紫色
            ]

            # st.markdown('<div class="token-options-container">', unsafe_allow_html=True)
            
            for i, option in enumerate(st.session_state.token_options[st.session_state.token_index]):
                color = colors[i % len(colors)]
                col1, _, col2 = st.columns([0.65, 0.05, 0.3])
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
                <h2>1. 「大语言模型」怎么写话的？</h2>
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

        tab2_l, _, tab2_r = st.columns([0.55, 0.05, 0.4])
        
        with tab2_l:
        # 第二步内容
            if st.session_state.current_step >= 1:
                st.markdown("""
                    <div class="fade-in">
                    <h2>2. 你觉得它是如何工作的？</h2>
                    </div>
                """, unsafe_allow_html=True)

                if "answers" not in st.session_state:
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
                    # 检查这个问题是否已经回答正确
                    question_key = f"q_{i}_correct"
                    if question_key not in st.session_state:
                        st.session_state[question_key] = False

                    answer = st.radio("", q["options"], key=f"q_{i}")

                    if st.button("提交", key=f"submit_{i}"):
                        is_correct = q["options"].index(answer) == q["correct"]
                        if is_correct and not st.session_state[question_key]:
                            st.success("✅ 回答正确！")
                            st.session_state[question_key] = True
                            update_score(st, "原理图解", 1)  # 只在首次回答正确时更新分数
                            st.session_state.caution_flag = 1
                        elif is_correct and st.session_state[question_key]:
                            st.success("✅ 回答正确！(已经获得过分数)")
                        else:
                            st.error("❌ 回答错误。")

                    if st.session_state.caution_flag != 0:
                        with st.expander("⚠️ 注意", expanded=False):  # expanded=True means it starts expanded
                            st.markdown("""
                                <div style="
                                    background-color: rgba(255, 190, 0, 0.1);
                                    border: 2px solid #ffbe00;
                                    border-radius: 15px;
                                    padding: 15px;">
                                    <p style="color: #fff; line-height: 1.6;">
                                        最新研究表明，虽然看起来大语言模型是生成一个显示一个，但在它的内部，有着像我们一样更复杂的「思考」，比如让它写一首诗，它会先考虑末尾字的押韵，先确定好最后一个字，再按顺序生成中间这部分词。发现这一点还多亏Anthropic公司的科学家们把大语言模型的「脑壳」打开后才观察到的。所以不能只凭观察到的现象来判断它的工作原理。
                                    </p>
                                </div>
                            """, unsafe_allow_html=True)

            # 显示当前章节得分
            score_status = get_score_status(st)
            st.sidebar.markdown(f"### 本节得分: {score_status['sections']['原理图解']['score']}/{score_status['sections']['原理图解']['max']}")

            if st.session_state.current_step >= 2:
                st.markdown("""
                    <div class="fade-in">
                    <h2>3.大语言模型是怎么猜出每个备选词的？</h2>
                    </div>
                """, unsafe_allow_html=True)

                pretraining_l, pretraining_r = st.columns([0.05, 0.95])
                with pretraining_l:
                    st.subheader("📚")
                with pretraining_r:
                    st.markdown("""
                        <h2 class="gradient-text">读书破万卷，下笔如有神！—— 「预训练」！</h2>
                    """, unsafe_allow_html=True)

                with st.expander("🎓 小知识", expanded=False):  # expanded=True means it starts expanded
                    st.markdown("""
                        <div style="
                            background-color: rgba(180, 255, 0,0.1);
                            border: 2px solid #9bff00;
                            border-radius: 15px;
                            padding: 15px;">
                            <p style="color: #fff; line-height: 1.6; font-size: 1.2em;">
                                如果一个人去读GPT-4预训练所用数据（约13万亿个词元），即便24小时不停的阅读，大概需要8.2万年才能读完！🤯
                            </p>
                        </div>
                    """, unsafe_allow_html=True)

                st.session_state.image_flag = 1
            
            # 第三步内容
            if st.session_state.current_step >= 3:
                st.markdown("""
                    <div class="fade-in">
                    <h2>4.究竟是按字，还是按词生成呢？</h2>
                    </div>
                """, unsafe_allow_html=True)
                

            # 下一步按钮
            if st.session_state.current_step < 3:  # 最多显示两个主题
                if st.button("下一步 ▶", key="next_button"):
                    st.session_state.current_step += 1
                    st.rerun()

        with tab2_r:
            if st.session_state.image_flag != 0:
                # Define the list of images and their captions
                images = [
                    {'path': './images/Readbooks.png', 'caption': '图像由AI生成'},
                    {'path': './images/WritingKid.png', 'caption': '图像由AI生成'},
                    {'path': './images/Pretraining.png', 'caption': '图像由AI生成'},
                    # Add more images as needed
                ]
                
                # Initialize the image index in session state if not exists
                if 'carousel_index' not in st.session_state:
                    st.session_state.carousel_index = 0
                
                # Create columns for navigation buttons and image
                col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
                
                # Previous button
                with col1:
                    if st.button("◀"):
                        st.session_state.carousel_index = (st.session_state.carousel_index - 1) % len(images)
                        st.rerun()
                
                # Display current image
                with col2:
                    current_image = images[st.session_state.carousel_index]
                    st.image(
                    current_image['path'],
                    use_container_width=True,
                    caption=f"图像 {st.session_state.carousel_index + 1}/{len(images)}: {current_image['caption']}"
                    )
                
                # Next button
                with col3:
                    if st.button("▶"):
                        st.session_state.carousel_index = (st.session_state.carousel_index + 1) % len(images)
                        st.rerun()
                
                # Display navigation dots
                dots_html = '<div style="text-align: center; margin-top: 10px;">'
                for i in range(len(images)):
                    if i == st.session_state.carousel_index:
                        dots_html += '●' + '&nbsp;'
                    else:
                        dots_html += '○' + '&nbsp;'
                dots_html += '</div>'
                st.markdown(dots_html, unsafe_allow_html=True)
                
                st.session_state.image_flag = 0

    with tabs[0]:
        col_tab = st.columns([0.4, 0.05, 0.55])

        with col_tab[2]:
            st.markdown("")
            blocks = [
                ("写作文的过程", "h1"),
                ("---", "p"),
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
                render_svg('images/DiaryNew.svg', caption="图像来源：由AI生成")

        with col_tab[0]:
            st.image('./images/writingBoy.png', use_container_width=True, caption="图像为AI生成")

        # 添加下一步按钮
        if st.button("下一步", key="next_block"):
            if st.session_state.block_index < len(blocks):
                st.session_state.block_index += 1
                st.rerun()
    
    with tabs[3]:
        st.markdown("")
        title_l, title_r = st.columns([0.12, 0.88])
        with title_l:
            st.markdown("""
                    <h1 class="base-text">「词元」</h1>
                    """, unsafe_allow_html=True)
        with title_r:   
            st.markdown("""
                    <h1 class="gradient-text">能准确表达语义的最少的文字组合！</h1>
                    """, unsafe_allow_html=True)
            # st.divider()

        # 初始化分词状态
        if 'predictor' not in st.session_state:
            from model import LLMPredictor
            st.session_state.predictor = LLMPredictor()
            
        if 'tokenized' not in st.session_state:
            st.session_state.tokenized = False

        tab3_l, _, tab3_r = st.columns([0.5, 0.05, 0.45])
        with tab3_l:
            st.divider()
            st.subheader("💡举例：「今天」拆开后不能表示原来的意思！")
            st.markdown("- **今**：可能有「今晚」、「今年」等意思")
            st.markdown("- **天**：可能有「天气」、「天空」等意思")

            st.subheader("🤖 大语言模型以「词元」为最小单位，「逐个词元」生成！")

        with tab3_r:
            # 示例文本
            st.divider()
            sample_texts = {
                "中文": "今天天气真不错，我们一起去春游吧！",
                "英文": "The quick brown fox jumps over the lazy dog."
            }
            selected_lang = st.radio("选择语言", ["中文", "英文"], key="token_lang")
            user_text = st.text_input("输入要分析的文本", value=sample_texts[selected_lang])

        st.divider()
        if st.button("开始分词分析"):
            try:
                # 获取对应的模型和分词器
                model, tokenizer = st.session_state.predictor._get_model_and_tokenizer(selected_lang)
                
                # 对文本进行编码和解码
                encoded = tokenizer.encode(user_text)
                tokens = [tokenizer.decode([id]).strip() for id in encoded]
                
                # 使用不同的颜色显示tokens，增加颜色透明度
                colors = [
                    'rgba(255, 99, 132, 0.4)',   # 红色
                    'rgba(54, 162, 235, 0.4)',   # 蓝色
                    'rgba(255, 206, 86, 0.4)',   # 黄色
                    'rgba(75, 192, 192, 0.4)',   # 青色
                    'rgba(153, 102, 255, 0.4)',  # 紫色
                ]
                
                # 生成Token展示HTML，添加hover效果
                token_html = '<div class="token-container">'
                for i, token in enumerate(tokens):
                    color = colors[i % len(colors)]
                    token_html += f'''
                        <span class="token-item" style="
                            background-color: {color};
                            animation: tokenAppear 0.5s ease forwards;
                            animation-delay: {i * 0.15}s;
                            transition: transform 0.2s ease, box-shadow 0.2s ease;
                            cursor: pointer;
                            " onmouseover="this.style.transform='scale(1.1)';this.style.boxShadow='0 4px 8px rgba(0,0,0,0.2)'"
                            onmouseout="this.style.transform='scale(1)';this.style.boxShadow='0 2px 4px rgba(0,0,0,0.1)'">
                            {token}
                        </span>'''
                token_html += '</div>'
                
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