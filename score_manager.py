def init_score_state(st):
    """初始化分数相关的session state"""
    if "total_score" not in st.session_state:
        st.session_state.total_score = 0
    if "max_score" not in st.session_state:
        st.session_state.max_score = 0
    if "section_scores" not in st.session_state:
        st.session_state.section_scores = {
            "原理图解": {"score": 0, "max": 1},  # 1分
            "实践评估": {"score": 0, "max": 2}   # 2分
        }

def update_score(st, section, points):
    """更新指定部分的分数"""
    if section in st.session_state.section_scores:
        st.session_state.section_scores[section]["score"] += points
        # 更新总分
        st.session_state.total_score = sum(
            section["score"] for section in st.session_state.section_scores.values()
        )
        st.session_state.max_score = sum(
            section["max"] for section in st.session_state.section_scores.values()
        )

def get_score_status(st):
    """获取当前得分状态"""
    return {
        "total": st.session_state.total_score,
        "max": st.session_state.max_score,
        "sections": st.session_state.section_scores
    }
