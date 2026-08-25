import streamlit as st
from utils.auth import is_logged_in, get_current_user


MENU = [
    ("home", "홈", "app.py"),
    ("about", "서비스 설명", "pages/About.py"),
    ("test", "매칭 테스트", "pages/Matching_Test.py"),
    ("noti", "알림", "pages/Notifications.py"),
]


def render_header(active: str = "home"):
    with st.container(border=True):
        cols = st.columns([2.2, 1, 1, 1, 1, 1, 1.4])

        # 로고 + 서비스명
        with cols[0]:
            logo_col, title_col = st.columns([0.25, 1.75], gap="small")

            with logo_col:
                st.image("assets/logo.png", width=38)

            with title_col:
                st.markdown(
                    """
                    <div style="
                        font-size:21px;
                        font-weight:700;
                        color:#0D1B3D;
                        line-height:38px;
                        white-space:nowrap;
                    ">
                        이어질 숙명
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # 메뉴 버튼
        for col, (key, label, path) in zip(cols[1:6], MENU):
            prefix = "🔹 " if key == active else ""

            if col.button(
                f"{prefix}{label}",
                use_container_width=True,
                key=f"nav_{key}"
            ):
                st.switch_page(path)

        # 로그인 / 내 계정 버튼
        if is_logged_in():
            user = get_current_user()
            name = user.get("name", "사용자")

            if cols[6].button(
                f"👤 {name}",
                use_container_width=True,
                key="nav_account"
            ):
                st.switch_page("pages/Login.py")

        else:
            if cols[6].button(
                "로그인",
                use_container_width=True,
                type="primary",
                key="nav_login"
            ):
                st.switch_page("pages/Login.py")
