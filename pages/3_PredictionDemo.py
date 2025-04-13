import streamlit as st
from model import LLMPredictor
import time
import random  # 添加这一行

def main():
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
    </style>
    """, unsafe_allow_html=True)

    # 将模型实例存储在 session state 中
    if 'predictor' not in st.session_state:
        st.session_state.predictor = LLMPredictor()

    st.markdown('<h1 class="gradient-title">动手试试看：下一个「词元」预测</h1>', unsafe_allow_html=True)
    # st.markdown("<h3 style='text-align: center;'>英文模型：GPT-2，中文模型：Qwen2-1.5B，Top-K采样</h3>", unsafe_allow_html=True)

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
    if 'temp_highlight_token' not in st.session_state:  # 新增：用于临时高亮显示选中的词元
        st.session_state.temp_highlight_token = None

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

    # 添加自定义CSS样式
    st.markdown("""
        <style>
        /* 增大预测结果的字体大小 */
        .prediction-text {
            font-size: 1.6em !important;
            padding: 0 !important;
            margin: 0 !important;
        }
        
        /* 词元块样式 */
        .token-block {
            background: rgba(120, 120, 120, 0.15);
            border-radius: 10px;
            padding: 4px 15px;
            margin: 2px 0;
            border: 1px solid transparent;
            display: inline-block;
            width: 100%;
        }
        
        /* 自动模式下的选中效果 */
        .token-block.selected {
            background: rgba(255, 223, 0, 0.15);
            border: 2px solid rgba(255, 200, 0, 0.8);
        }
        </style>
    """, unsafe_allow_html=True)

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

            # st.markdown("<h3 class='prediction-text'>候选「词元」及其概率：</h3>", unsafe_allow_html=True)
            
            # 显示预测结果
            for pred in result['predictions']:
                token = pred['token']
                prob = pred['probability']
                is_sampled = pred.get('is_sampled', True)
                
                # 修改选中类判断逻辑，增加手动模式下的临时高亮
                selected_class = ""
                if (is_sampled and st.session_state.is_auto_mode) or (not st.session_state.is_auto_mode and token == st.session_state.temp_highlight_token):
                    selected_class = "selected"
                
                cols = st.columns([2, 6, 1, 1])
                with cols[0]:
                    st.markdown(f"""
                        <div class='token-block {selected_class}'>
                            <div class='prediction-text'>{token}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with cols[1]:
                    st.progress(prob)

                with cols[2]:
                    # 修改概率显示颜色逻辑
                    prob_color = "#A9A9A9"  # 默认灰色
                    if (is_sampled and st.session_state.is_auto_mode) or (not st.session_state.is_auto_mode and token == st.session_state.temp_highlight_token):
                        prob_color = "#FFD700"  # 高亮显示为金色
                    
                    st.markdown(f"""
                        <div class='prediction-text' style='color: {prob_color};'>
                            {100 * prob:.2f}%
                        </div>
                    """, unsafe_allow_html=True)
                
                with cols[3]:
                    if not st.session_state.is_auto_mode:
                        if st.button("选择", key=f"use_{token}"):
                            # 设置临时高亮
                            st.session_state.temp_highlight_token = token
                            st.rerun()

            # 如果存在临时高亮的词元，等待后添加到文本
            if not st.session_state.is_auto_mode and st.session_state.temp_highlight_token:
                token = st.session_state.temp_highlight_token
                time.sleep(0.5)  # 延时0.5秒
                st.session_state.generated_text += token
                st.session_state.temp_highlight_token = None  # 清除临时高亮状态
                st.rerun()

            # 自动模式的代码保持不变
            if st.session_state.is_auto_mode and st.session_state.is_running:
                candidates = result['predictions']
                selected_token = [item['token'] for item in candidates if item['is_sampled']][0]
                st.session_state.selected_token = selected_token  # 更新选中的token
                st.session_state.generated_text += selected_token
                
                # 添加选中提示
                st.success(f"已选择「词元」: {selected_token}")
                
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
