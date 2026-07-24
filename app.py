import streamlit as st
from components.header import render_header
from components.footer import render_footer
from components.cards import action_card
import base64


st.set_page_config(
    page_title="이어질 숙명",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def image_to_base64(path: str):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# ---- 전역 세션 초기화 ----
def init_state():
    defaults = {
        "page": "home",
        "answers": {},
        "q_index": 0,
        "result": None,
        "selected_mentor": None,
        "active_conversation": None,
        "match_request": None,
        "demo_messages": [],
    }

    for k, v in defaults.items():
        st.session_state.setdefault(k, v)


init_state()


# ---- 페이지 이동 헬퍼 ----
def go(page_path: str):
    st.switch_page(page_path)


# ---- 공통 헤더 ----
render_header(active="home")


# ---- 메인 히어로 섹션 ----
st.markdown("<br>", unsafe_allow_html=True)

hero_left, hero_right = st.columns([1.05, 0.95], vertical_alignment="center")

with hero_left:
    logo_base64 = image_to_base64("assets/logo.png")

    st.markdown(
        f"""
        <div style="
            display:flex;
            align-items:center;
            gap:8px;
            margin-bottom:8px;
        ">
            <img src="data:image/png;base64,{logo_base64}"
                 style="width:68px; height:68px; object-fit:contain;">
            <h1 style="
                font-size:46px;
                margin:0;
                color:#0D1B3D;
                line-height:1;
            ">
                이어질 숙명
            </h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <p style="font-size:28px; font-weight:700; color:#0D1B3D; 
                  margin-top:22px; line-height:1.45;">
            연결에서 성장으로,<br>
            이어질 우리의 가능성
        </p>

        <p style="font-size:17px; color:#555; line-height:1.8; margin-top:16px;">
            숙명여대 선배와 후배가 만나<br>
            학교생활, 전공, 진로 고민을 함께 나누고 성장하는<br>
            멘토·멘티 매칭 서비스입니다.
        </p>
        """,
        unsafe_allow_html=True,
    )

with hero_right:
    st.image("assets/mainimg.png", use_container_width=True)


st.divider()


# ---- 서비스 기능 카드 ----
a1, a2, a3 = st.columns(3)

with a1:
    if action_card(
        "매칭 테스트",
        "5개의 질문으로 나의 성향 유형을 확인하고 나에게 맞는 선배를 찾아보세요."
    ):
        go("pages/Matching_Test.py")
with a2:
    if action_card(
        "멘토 등록하기",
        "선배로서 이어질 숙명에 참여하여 후배들과 지식과 경험을 나누세요."
    ):
        go("pages/Mentor_Register.py")

with a3:
    if action_card(
        "서비스 설명 보기",
        "이어질 숙명이 어떤 서비스인지, 어떤 흐름으로 이용하는지 알아보세요."
    ):
        go("pages/About.py")




render_footer()