import streamlit as st

from components.header import render_header
from components.footer import render_footer

st.set_page_config(
    page_title="서비스 설명 · 이어질 숙명",
    page_icon="💙",
    layout="wide"
)

render_header(active="about")

st.title("서비스 설명")
st.divider()


# -----------------------------
# 서비스 소개
# -----------------------------
with st.container(border=True):
    st.subheader("이어질 숙명은 어떤 서비스인가요?")
    st.write(
        "이어질 숙명은 숙명여대 학생들이 전공, 진로, 학교생활 고민을 나눌 수 있도록 "
        "선배와 후배를 연결하는 멘토·멘티 매칭 서비스입니다."
    )

st.write("")


# -----------------------------
# 왜 필요할까요?
# -----------------------------
with st.container(border=True):
    st.subheader("왜 필요할까요?")
    st.markdown(
        """
        ① 선배와 연결될 기회가 부족해요.  
        ② 전공과 진로 정보를 얻는 데 어려움이 있어요.  
        ③ 누구에게 물어봐야 할지 몰라 혼자 고민하는 경우가 많아요.
        """
    )

st.write("")


# -----------------------------
# 이용 흐름
# -----------------------------
st.subheader("이용 흐름")

c1, c2 = st.columns(2)

with c1:
    with st.container(border=True):
        st.markdown("### 멘티로 이용하기")
        st.markdown(
            """
            1. 매칭 테스트 응답  
            2. 나의 송이 유형 확인  
            3. 추천 멘토 카드 확인  
            4. 매칭 신청 후 수락되면 채팅 시작
            """
        )

with c2:
    with st.container(border=True):
        st.markdown("### 멘토로 참여하기")
        st.markdown(
            """
            1. 멘토 등록 페이지에서 정보 입력  
            2. 도움 가능 분야와 추천 후배 유형 선택  
            3. 후배의 매칭 신청 확인  
            4. 수락 후 채팅으로 멘토링 시작
            """
        )

st.write("")


# -----------------------------
# 핵심 기능 소개
# -----------------------------
st.subheader("핵심 기능 소개")

f1, f2, f3 = st.columns(3)

with f1:
    with st.container(border=True):
        st.markdown("### 매칭 테스트")
        st.write("질문 기반으로 나의 성향 유형을 분석해요.")

with f2:
    with st.container(border=True):
        st.markdown("### 멘토 등록")
        st.write("멘토로 참여하고 싶은 학생은 도움 가능 분야를 등록할 수 있어요.")

with f3:
    with st.container(border=True):
        st.markdown("### 채팅 연결")
        st.write("매칭이 수락되면 선후배가 직접 대화를 시작할 수 있어요.")

st.write("")


# -----------------------------
# 이용 방법 안내
# -----------------------------
with st.container(border=True):
    st.subheader("이용 방법 안내")
    st.markdown(
        """
        1. 학교 이메일로 로그인 또는 회원가입  
        2. 멘티는 매칭 테스트를 통해 추천 멘토 확인  
        3. 멘토는 멘토 등록 페이지에서 정보 입력  
        4. 매칭 요청이 수락되면 채팅 시작
        """
    )

st.write("")


# -----------------------------
# CTA 버튼
# -----------------------------
st.markdown("### 나에게 맞는 연결을 시작해볼까요?")

b1, b2 = st.columns(2)

with b1:
    if st.button("매칭 테스트 시작하기", type="primary", use_container_width=True):
        st.switch_page("pages/Matching_Test.py")

with b2:
    if st.button("멘토 등록하기", type="primary", use_container_width=True):
        st.switch_page("pages/Mentor_Register.py")

render_footer()