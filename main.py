import streamlit as st
from model import LLMPredictor
import time

def main():
    # 将模型实例存储在 session state 中
    if 'predictor' not in st.session_state:
        st.session_state.predictor = LLMPredictor()

    st.title("下一个词元预测演示")
    st.subheader("英文模型：GPT-2，中文模型：Qwen2-1.5B，Top-K采样")

    # 初始化其他 session state
    if 'generated_text' not in st.session_state:
        st.session_state.generated_text = ""  # 初始化为空字符串
    if 'default_prompts' not in st.session_state:
        st.session_state.default_prompts = {
            "中文": "请输入中文文本",
            "英文": "Please input English text"
        }
    if 'is_auto_mode' not in st.session_state:
        st.session_state.is_auto_mode = False
    if 'is_running' not in st.session_state:
        st.session_state.is_running = False
    if 'predicting' not in st.session_state:
        st.session_state.predicting = False
    if 'temperature' not in st.session_state:
        st.session_state.temperature = 1.0
    if 'top_k' not in st.session_state:
        st.session_state.top_k = 5
    if 'token_len' not in st.session_state:
        st.session_state.token_len = 0
    if 'model_lang' not in st.session_state:
        st.session_state.model_lang = "中文"
    if 'selected_token' not in st.session_state:
        st.session_state.selected_token = None  # 新增：追踪选中的token
    if 'generation_interval' not in st.session_state:
        st.session_state.generation_interval = 0.5  # 添加默认生成间隔

    # 添加设置区域
    with st.sidebar:
        st.header("模型设置")
        
        # 复位按钮 - 现在只清空文本而不是设置固定值
        if st.button("清空文本", type="primary"):
            st.session_state.generated_text = ""
            st.session_state.is_running = False
            st.session_state.predicting = False
            st.rerun()

        # 分隔线
        st.divider()
        
        # 自动/手动模式切换
        st.session_state.is_auto_mode = st.toggle("自动模式", value=st.session_state.is_auto_mode)
        
        if st.session_state.is_auto_mode:
            # 自动模式的启动/停止控制
            if not st.session_state.is_running:
                if st.button("开始自动生成"):
                    st.session_state.is_running = True
                    st.rerun()
            else:
                if st.button("停止生成"):
                    st.session_state.is_running = False
                    st.rerun()
            
            # 修改生成速度控制的实现
            generation_interval = st.slider(
                "生成间隔 (秒)",
                min_value=0.1,
                max_value=2.0,
                value=st.session_state.generation_interval,
                step=0.1,
                key="interval_slider",
                help="每个token生成之间的时间间隔"
            )
            # 确保更新到 session state
            if generation_interval != st.session_state.generation_interval:
                st.session_state.generation_interval = generation_interval

        # 模型语言选择
        try:
            model_lang = st.selectbox(
                "选择模型语言",
                ["中文", "英文"],
                index=0 if st.session_state.model_lang == "中文" else 1
            )
            if model_lang != st.session_state.model_lang:
                with st.spinner(f"正在切换到{model_lang}模型..."):
                    st.session_state.model_lang = model_lang
                    if not st.session_state.generated_text.strip():  # 只在文本为空时显示提示
                        st.session_state.generated_text = st.session_state.default_prompts[model_lang]
                    # 重置预测状态
                    st.session_state.predicting = False
                    st.session_state.is_running = False
                    st.rerun()

        except Exception as e:
            st.error(f"模型切换失败: {str(e)}")

        # 温度控制
        st.session_state.temperature = st.slider(
            "温度 (Temperature)",
            min_value=0.1,
            max_value=2.0,
            value=st.session_state.temperature,
            step=0.1,
            help="较高的温度会产生更多样化的输出，较低的温度会产生更确定性的输出"
        )

        st.session_state.top_k = st.slider(
            "Top-K 采样",
            min_value=1,
            max_value=20,
            value=st.session_state.top_k,
            step=1,
            help="在词表中选择排在最前的K个词"
        )

        # 分割线
        st.divider()

        # 词库长度显示
        try:
            if st.session_state.model_lang == "中文":
                token_len = (st.session_state.predictor.zh_tokenizer.vocab_size 
                           if st.session_state.predictor.zh_tokenizer is not None 
                           else "模型未加载")
            else:
                token_len = (st.session_state.predictor.en_tokenizer.vocab_size 
                           if st.session_state.predictor.en_tokenizer is not None 
                           else "模型未加载")
            
            # 更新session state中的token_len
            st.session_state.token_len = token_len
        except Exception as e:
            st.session_state.token_len = "无法获取词表大小"
            st.error(f"获取词表大小时出错: {str(e)}")

        st.markdown("#### 词库的长度")  # Using markdown for black text
        st.text_area(
            "",  # Remove label since we're using markdown above
            value=str(st.session_state.token_len),  # Ensure value is string
            disabled=True,
            height=100,
            key="vocab_size_area",
            label_visibility="collapsed",  # Hide empty label
        )
        # Apply custom CSS to increase text size
        st.markdown("""
            <style>
            div[data-testid="stTextArea"] textarea {
                font-size: 1.2em;
            }
            </style>
            """, unsafe_allow_html=True)

    # 文本显示区域，添加最大长度限制
    if len(st.session_state.generated_text) > 1000:  # 防止生成文本过长
        st.warning("文本已达到最大长度限制，请点击复位按钮开始新的生成")
        st.session_state.is_running = False
        st.session_state.predicting = False

    # 修改预测逻辑，添加温度参数
    def update_predictions():
        try:
            result = st.session_state.predictor.generate_next_token(
                input_text=st.session_state.generated_text,
                temperature=st.session_state.temperature,
                model_lang=st.session_state.model_lang,
                top_k=st.session_state.top_k
            )
            
            if not result:
                st.error("预测失败，请检查模型加载状态")
                return

            st.subheader("候选 Tokens 及其概率：")
            
            # 显示预测结果
            for pred in result['predictions']:
                token = pred['token']
                prob = pred['probability']
                is_sampled = pred.get('is_sampled', True)  # 获取是否被采样选中
                
                # 创建一个带有背景色的列布局
                col_style = "background-color: #90EE90;" if is_sampled else ""
                cols = st.columns([2, 6, 2])
                with cols[0]:
                    if is_sampled:
                        st.markdown(f"**:green[Token: {token}]** 🎯")
                    else:
                        st.write(f"Token: {token}")
                with cols[1]:
                    progress_container = st.container()
                    with progress_container:
                        progress_bar = st.progress(0)
                        progress_bar.progress(prob)
                with cols[2]:
                    if is_sampled:
                        st.markdown(f"**:green[{prob:.5f}]**")
                    else:
                        st.write(f"{prob:.5f}")
                    if not st.session_state.is_auto_mode:
                        if st.button("选择", key=f"use_{token}", help=f"点击将'{token}'添加到文本中"):
                            st.session_state.generated_text += token
                            st.rerun()

            if st.session_state.is_auto_mode and st.session_state.is_running:
                candidates = result['predictions']
                selected_token = [item['token'] for item in candidates if item['is_sampled']][0]
                st.session_state.selected_token = selected_token  # 更新选中的token
                st.session_state.generated_text += selected_token
                
                # 添加选中提示
                st.success(f"已选择Token: {selected_token}")
                
                time.sleep(st.session_state.generation_interval)
                st.rerun()

        except Exception as e:
            st.error(f"发生错误: {str(e)}")
            st.write("Error details:", str(e))
            st.session_state.is_running = False
            st.session_state.predicting = False

    # 文本显示区域
    new_text = st.text_area(
        "输入文本：",  # 更改标签更明确
        value=st.session_state.generated_text,
        height=100,
        key="text_input_area",
        placeholder=st.session_state.default_prompts[st.session_state.model_lang],  # 添加占位符提示
        disabled=st.session_state.is_running or st.session_state.predicting
    )

    # 仅当文本非空时才允许预测
    if new_text.strip():
        # 如果文本被用户修改，更新 session state
        if new_text != st.session_state.generated_text:
            st.session_state.generated_text = new_text
            st.session_state.predicting = False
            st.session_state.is_running = False

        # 显示预测按钮和结果
        if st.session_state.is_auto_mode:
            st.info("当前处于自动模式")
            if st.session_state.is_running:
                st.success("正在自动生成中...")
                update_predictions()
            else:
                st.warning("自动生成已暂停")
        else:
            if st.button("预测下一个词"):
                st.session_state.predicting = True
            
            if st.session_state.predicting:
                update_predictions()
    else:
        st.warning("请先输入一些文本再开始预测")

if __name__ == '__main__':
    main()