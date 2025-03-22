import streamlit as st
import plotly.graph_objects as go
import numpy as np
from score_manager import init_score_state, update_score, get_score_status
import random, time

def create_ball_box(balls_data, color_map):
    # 创建物理引擎模拟的小球箱子
    fig = go.Figure()
    box_width = 400
    box_height = 400
    
    # 随机生成小球位置
    positions = []
    for ball_name, count in balls_data.items():
        for _ in range(count):
            x = random.randint(50, box_width-50)
            y = random.randint(50, box_height-50)
            positions.append((x, y, color_map[ball_name]))
    
    # 添加小球
    for x, y, color in positions:
        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode='markers',
            marker=dict(size=20, color=color),
            showlegend=False
        ))
    
    # 设置布局
    fig.update_layout(
        width=box_width,
        height=box_height,
        plot_bgcolor='rgba(240, 240, 240, 0.8)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(l=0, r=0, t=0, b=0)
    )
    return fig

def sample_one_ball(balls_data):
    """单次抽样一个球"""
    total_balls = sum(balls_data.values())
    rand_num = random.random() * total_balls
    curr_sum = 0
    for color, count in balls_data.items():
        curr_sum += count
        if rand_num <= curr_sum:
            return color
    return list(balls_data.keys())[0]  # 保险起见，返回第一个颜色

def sampling_simulation(balls_data, n_times):
    """连续抽取n次，返回所有结果"""
    results = []
    for _ in range(n_times):
        results.append(sample_one_ball(balls_data))
    return results

def adjust_balls(balls_data, changed_color, new_value):
    """自动调节球的数量，保持总数为100"""
    # 颜色优先级（从最后调节到最先调节）
    priority = ["红球 🔴", "蓝球 🔵", "绿球 🟢", "黄球 🟡", "紫球 🟣"]
    
    # 计算当前总数
    total = sum(balls_data.values())
    diff = total - 100
    
    # 如果需要调节
    if diff != 0:
        # 从优先级最低的球开始调节
        for color in reversed(priority):
            if color == changed_color:
                continue
            
            current = balls_data[color]
            if diff > 0:  # 需要减少球数
                # 计算可以减少的数量（保留至少1个球）
                can_reduce = max(0, current - 1)
                reduce = min(can_reduce, diff)
                balls_data[color] -= reduce
                diff -= reduce
            else:  # 需要增加球数
                balls_data[color] -= diff  # diff是负数，所以用减法
                diff = 0
            
            if diff == 0:
                break
    
    return balls_data

def display_results(container, total_sampling_results, colors):
    """显示当前抽样结果的柱状图"""
    total_samples = sum(total_sampling_results.values())
    if total_samples > 0:
        fig = go.Figure()
        for ball_name, count in total_sampling_results.items():
            percentage = (count / total_samples * 100)
            fig.add_trace(go.Bar(
                y=[ball_name],
                x=[count],
                orientation='h',
                marker_color=colors[ball_name],
                width=0.6,
                text=f"{count}次 ({percentage:.1f}%)",
                textposition='inside',
                insidetextanchor='start',
                textfont=dict(color='black', size=14)
            ))
        
        fig.update_layout(
            height=300,
            showlegend=False,
            xaxis_title="抽样次数",
            yaxis=dict(
                autorange="reversed",
                side='left'
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=150, r=20, t=20, b=40),
            bargap=0.2,
            uniformtext=dict(mode='hide', minsize=12)
        )
        
        container.plotly_chart(fig, use_container_width=False)

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
            font-size: 7em;
            font-weight: 1000;
            text-align: center;
            padding: 20px 0;
            margin-bottom: 30px;
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
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="gradient-title">游戏中的知识</h1>', unsafe_allow_html=True)
    
    tabs = st.tabs(["概率抽样", "总结"])
    
    with tabs[0]:
        st.header("概率抽样")
        
        # 创建左右分栏
        left_col, right_col = st.columns([6, 4])
        
        with left_col:
            st.subheader("设置参数")
            
            # 定义颜色及其初始值
            colors = {
                "红球 🔴": "#FF4B4B",
                "蓝球 🔵": "#1E90FF",
                "绿球 🟢": "#32CD32",
                "黄球 🟡": "#FFD700",
                "紫球 🟣": "#9370DB"
            }
            
            if 'balls_data' not in st.session_state:
                st.session_state.balls_data = {color: 20 for color in colors.keys()}
                
            if 'sampling_results' not in st.session_state:
                st.session_state.sampling_results = {}
            
            # 滑动条控制小球数量
            total_balls = 0
            for ball_name, color_code in colors.items():
                col1, col2 = st.columns([7, 3])
                with col1:
                    value = st.slider(
                        f"{ball_name}数量",
                        1, 100,  # 最小值改为1
                        st.session_state.balls_data[ball_name],
                        key=f"slider_{ball_name}",
                        help="拖动滑块设置小球数量",
                        args=(color_code,)
                    )
                    
                    # 如果值发生变化，进行自动调节并重置抽样结果
                    if value != st.session_state.balls_data[ball_name]:
                        st.session_state.balls_data[ball_name] = value
                        st.session_state.balls_data = adjust_balls(
                            st.session_state.balls_data,
                            ball_name,
                            value
                        )
                        # 重置抽样结果
                        st.session_state.total_sampling_results = {color: 0 for color in colors.keys()}
                        # 强制更新页面
                        st.rerun()
                        
                with col2:
                    current_value = st.session_state.balls_data[ball_name]
                    st.markdown(f"**{current_value}个 ({current_value}%)**")
                total_balls += st.session_state.balls_data[ball_name]
            
        with right_col:
            # 球箱预览部分保持不变
            st.subheader("球箱预览")
            if total_balls == 100:
                fig = create_ball_box(st.session_state.balls_data, colors)
                st.plotly_chart(fig, use_container_width=True, key="box_preview")
            else:
                st.warning("请确保总球数为100个")
            
            # 在右侧创建柱状图容器
            chart_container = st.empty()
            st.markdown("---")
            if 'total_sampling_results' not in st.session_state:
                st.session_state.total_sampling_results = {color: 0 for color in colors.keys()}
            display_results(chart_container, st.session_state.total_sampling_results, colors)

        with left_col:
            st.markdown("---")
            # 抽样控制部分
            st.number_input(
                "设置每次点击抽取的球数",
                min_value=1,
                value=10,
                key="batch_size"
            )
            
            # 将两个按钮放在同一行
            button_cols = st.columns(2)
            with button_cols[0]:
                sample_button = st.button("连续抽取", key="sample_button", use_container_width=True)
            with button_cols[1]:
                reset_button = st.button("重置抽样结果", key="reset_button", use_container_width=True)
            
            # 处理按钮点击事件
            if reset_button:
                st.session_state.total_sampling_results = {color: 0 for color in colors.keys()}
                st.rerun()
                
            if total_balls == 100 and sample_button:
                batch_size = st.session_state.batch_size
                # 执行抽样并实时更新结果
                for _ in range(batch_size):
                    result = sample_one_ball(st.session_state.balls_data)
                    st.session_state.total_sampling_results[result] += 1
                    display_results(chart_container, st.session_state.total_sampling_results, colors)
                    time.sleep(0.05)
                
                # 显示本次抽样结果统计
                st.write("本次抽样结果：")
                current_results = {color: 0 for color in colors.keys()}
                for _ in range(batch_size):
                    color = sample_one_ball(st.session_state.balls_data)
                    current_results[color] += 1
                
                for color, count in current_results.items():
                    if count > 0:
                        st.write(f"{color}: {count}个")

    with tabs[1]:
        st.header("总结")
        # 这里添加总结的内容

if __name__ == "__main__":
    main()