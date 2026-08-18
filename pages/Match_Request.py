import streamlit as st

st.title("멘토링 매칭 신청")
st.write("신청서 페이지가 정상적으로 연결되었습니다.")

st.subheader("기본 신청 정보")

role = st.radio(
    "어떤 역할로 참여하시나요?",
    ["멘토", "멘티"]
)

st.subheader("이번 매칭에서 가장 원하는 것은 무엇인가요?")

if role == "멘티":
    topic_options = [
        "전공/학과 정보",
        "학교생활 조언",
        "수강신청/시간표",
        "대학생활 적응",
        "진로/취업",
        "동아리/대외활동",
        "기타"
    ]
else:
    topic_options = [
        "전공 경험 공유",
        "학교생활 조언",
        "진로 경험 공유",
        "공부/학업 도움",
        "대외활동 경험 공유",
        "대학생활 팁",
        "기타"
    ]

topics = st.multiselect(
    "희망 분야를 선택하세요",
    topic_options
)

st.subheader("활동 가능 시간")

preferred_time = st.multiselect(
    "가능한 시간을 선택하세요",
    [
        "평일 오전",
        "평일 오후",
        "평일 저녁",
        "주말 오전",
        "주말 오후",
        "주말 저녁"
    ]
)

st.subheader("선호하는 활동 방식")

activity_type = st.radio(
    "활동 방식을 선택하세요",
    ["대면", "비대면", "둘 다 가능"]
)

st.subheader("자기소개")

introduction = st.text_area(
    "간단한 자기소개를 입력하세요"
)

st.subheader("연락처 정보")

contact_type = st.selectbox(
    "연락처 종류",
    ["카카오톡", "인스타그램", "이메일", "기타"]
)

contact_value = st.text_input(
    "연락처를 입력하세요"
)

if st.button("신청서 확인"):
    if not topics:
        st.error("희망 분야를 하나 이상 선택해주세요.")
    elif not preferred_time:
        st.error("활동 가능 시간을 하나 이상 선택해주세요.")
    elif not introduction.strip():
        st.error("자기소개를 입력해주세요.")
    elif not contact_value.strip():
        st.error("연락처를 입력해주세요.")
    else:
        st.success("신청서 입력 화면이 정상적으로 작동합니다.")

        st.write("선택한 역할:", role)
        st.write("희망 분야:", ", ".join(topics))
        st.write("활동 가능 시간:", ", ".join(preferred_time))
        st.write("활동 방식:", activity_type)
        st.write("자기소개:", introduction)
        st.write("연락처 종류:", contact_type)
        st.write("연락처:", contact_value)
