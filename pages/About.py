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
    st.write(
        "매칭 테스트를 통해 나에게 맞는 유형을 확인하고, "
        "추천 멘토에게 멘토링 신청서를 보낼 수 있어요."
    )

st.write("")


# -----------------------------
# 왜 필요할까요?
# -----------------------------
with st.container(border=True):
    st.subheader("왜 필요할까요?")
    st.markdown(
        """
        ① 선배와 자연스럽게 연결될 기회가 부족해요.  
        ② 전공, 진로, 학교생활 정보를 얻는 데 어려움이 있어요.  
        ③ 누구에게 물어봐야 할지 몰라 혼자 고민하는 경우가 많아요.  
        ④ 나와 비슷한 고민을 먼저 겪은 선배의 경험이 필요해요.
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
            1. 로그인 또는 회원가입  
            2. 매칭 테스트 응답  
            3. 나의 송이 유형 확인  
            4. 추천 멘토 카드 확인  
            5. 원하는 멘토에게 멘토링 신청서 제출  
            6. 알림 페이지에서 신청 상태 확인  
            7. 멘토가 수락하면 오픈채팅방 정보 확인
            """
        )

with c2:
    with st.container(border=True):
        st.markdown("### 멘토로 참여하기")
        st.markdown(
            """
            1. 로그인 또는 회원가입  
            2. 멘토 등록 페이지에서 정보 입력  
            3. 도움 가능 분야와 추천 후배 유형 선택  
            4. 오픈채팅방 링크 등록  
            5. 알림 페이지에서 후배의 신청서 확인  
            6. 신청을 수락할 때 오픈채팅방 비밀번호 입력  
            7. 멘티에게 오픈채팅방 입장 정보 전달
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
        st.write(
            "간단한 질문을 통해 나의 고민과 성향을 분석하고, "
            "나에게 맞는 송이 유형을 확인할 수 있어요."
        )

with f2:
    with st.container(border=True):
        st.markdown("### 멘토 등록")
        st.write(
            "멘토로 참여하고 싶은 학생은 도움 가능 분야, 추천 후배 유형, "
            "멘토링 가능 시간 등을 등록할 수 있어요."
        )

with f3:
    with st.container(border=True):
        st.markdown("### 멘토링 신청서")
        st.write(
            "추천 멘토에게 바로 신청하는 것이 아니라, "
            "궁금한 점과 희망 일정을 담은 신청서를 작성해 보낼 수 있어요."
        )

st.write("")

f4, f5, f6 = st.columns(3)

with f4:
    with st.container(border=True):
        st.markdown("### 알림")
        st.write(
            "멘티는 내가 보낸 신청 현황을 확인하고, "
            "멘토는 받은 신청서를 확인해 수락하거나 거절할 수 있어요."
        )

with f5:
    with st.container(border=True):
        st.markdown("### 일정 선택")
        st.write(
            "멘토는 멘티가 제안한 일정 후보 중 가능한 시간을 선택해 "
            "멘토링을 수락할 수 있어요."
        )

with f6:
    with st.container(border=True):
        st.markdown("### 오픈채팅 연결")
        st.write(
            "멘토가 신청을 수락하면 멘티에게 오픈채팅방 링크와 비밀번호가 전달되어 "
            "멘토링을 이어갈 수 있어요."
        )

st.write("")


# -----------------------------
# 이용 방법 안내
# -----------------------------
with st.container(border=True):
    st.subheader("이용 방법 안내")
    st.markdown(
        """
        1. 학교 이메일로 로그인 또는 회원가입을 합니다.  
        2. 멘티는 매칭 테스트를 완료하고 추천 멘토를 확인합니다.  
        3. 원하는 멘토에게 멘토링 신청서를 작성해 보냅니다.  
        4. 멘토는 알림 페이지에서 신청서를 확인하고 수락 또는 거절합니다.  
        5. 멘토가 수락하면 멘티는 알림 페이지에서 오픈채팅방 입장 정보를 확인합니다.  
        6. 멘토로 참여하고 싶은 학생은 멘토 등록 페이지에서 정보를 등록할 수 있습니다.
        """
    )

st.write("")


# -----------------------------
# 주의사항
# -----------------------------
with st.container(border=True):
    st.subheader("이용 시 참고해주세요")
    st.markdown(
        """
        - 멘토링 신청서는 멘토가 신청 내용을 미리 확인할 수 있도록 작성됩니다.  
        - 오픈채팅방 정보는 멘토가 신청을 수락한 뒤에만 멘티에게 전달됩니다.  
        - 멘토링 일정과 방식은 멘토와 멘티가 서로 조율하여 진행합니다.
        """
    )

st.write("")


# -----------------------------
# CTA 버튼
# -----------------------------
st.markdown("### 나에게 맞는 연결을 시작해볼까요?")

b1, b2 = st.columns(2)

with b1:
    if st.button(
        "매칭 테스트 시작하기",
        type="primary",
        use_container_width=True
    ):
        st.switch_page("pages/Matching_Test.py")

with b2:
    if st.button(
        "멘토 등록하기",
        type="primary",
        use_container_width=True
    ):
        st.switch_page("pages/Mentor_Register.py")


render_footer()
