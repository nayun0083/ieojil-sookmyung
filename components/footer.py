import streamlit as st

def render_footer():
    st.divider()
    st.markdown(
        """
        <div style="text-align:center; color:#999; font-size:13px; padding:16px 0;">
            이어질 숙명 · 숙명여자대학교 멘토·멘티 매칭 서비스<br>
            © 2026 Sookmyung Mentoring Team. All rights reserved.<br>
        </div>
        """,
        unsafe_allow_html=True,
    )
