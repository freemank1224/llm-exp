def init_score_state(st):
    """初始化分数相关的session state"""
    if 'sections' not in st.session_state:
        st.session_state.sections = {
            "问题引入": {"score": 0, "max": 1},     # 添加问题引入章节
            "原理图解": {"score": 0, "max": 1},
            "实践评估": {"score": 0, "max": 2},
            "游戏中的知识": {"score": 0, "max": 2}  # 总分：抽样操作1分 + 两道题各2分
        }
        st.session_state.total_score = 0
        st.session_state.max_score = sum(section["max"] for section in st.session_state.sections.values())

def update_score(st, section, points):
    """更新指定部分的分数"""
    if section in st.session_state.sections:
        st.session_state.sections[section]["score"] += points
        # 更新总分
        st.session_state.total_score = sum(
            section["score"] for section in st.session_state.sections.values()
        )
        st.session_state.max_score = sum(
            section["max"] for section in st.session_state.sections.values()
        )

def reset_section_score(st, section):
    """重置指定章节的分数"""
    if section in st.session_state.sections:
        # 从总分中减去该章节的分数
        st.session_state.total_score -= st.session_state.sections[section]["score"]
        # 重置该章节分数
        st.session_state.sections[section]["score"] = 0

def get_score_status(st):
    """获取当前得分状态"""
    return {
        "total": st.session_state.total_score,
        "max": st.session_state.max_score,
        "sections": st.session_state.sections
    }
