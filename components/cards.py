import streamlit as st

def notice_card(title: str, desc: str, badge: str = ""):
    with st.container(border=True):
        if badge:
            st.markdown(f"`{badge}`")
        st.markdown(f"**{title}**")
        st.caption(desc)

def action_card(title: str, desc: str, emoji: str = "✨") -> bool:
    with st.container(border=True):
        st.markdown(f"### {emoji} {title}")
        st.write(desc)
        return st.button(f"{title} →", use_container_width=True, type="primary",
                         key=f"action_{title}")

def mentor_card(mentor: dict):
    """추천 멘토 카드"""
    with st.container(border=True):
        st.markdown(f"### 👩‍🎓 {mentor['name']}")
        st.write(f"**학과:** {mentor['dept']}")
        st.write(f"**학번:** {mentor['sid']}")
        st.write(f"**관심 분야:** {mentor['field']}")
