import streamlit as st
from supabase_client import supabase


st.title("멘토 등록")

st.write("멘토로 활동하기 위한 정보를 입력해주세요.")


# 이름
name = st.text_input("이름")


# 이메일
email = st.text_input("이메일")


# 학과
dept = st.text_input("학과")


# 학년
grade = st.number_input(
    "학년",
    min_value=1,
    max_value=4,
    value=1
)


# 도움 가능 분야
field = st.text_input(
    "도움 가능 분야",
    placeholder="예: Python, 웹 개발, 전공 공부"
)


# 추천 후배 유형
mentor_type = st.text_input(
    "추천 후배 유형",
    placeholder="예: 전공·진로에 관심 있는 후배"
)


# 멘토링 가능 시간
available_time = st.text_input(
    "멘토링 가능 시간",
    placeholder="예: 평일 오후"
)


# 멘토 소개
intro = st.text_area(
    "멘토 소개",
    placeholder="자신을 자유롭게 소개해주세요."
)


# 등록 버튼
if st.button("멘토 등록하기"):

    if not name or not email or not dept:

        st.warning("이름, 이메일, 학과는 입력해주세요.")

    else:

        data = {
            "user_id": "00000000-0000-0000-0000-000000000000",
            "name": name,
            "email": email,
            "dept": dept,
            "grade": grade,
            "field": field,
            "type": mentor_type,
            "available_time": available_time,
            "intro": intro,
            "status": "pending"
        }

        try:

            response = (
                supabase
                .table("mentor_profiles")
                .insert(data)
                .execute()
            )

            st.success("멘토 등록이 완료되었습니다!")

        except Exception as e:

            st.error(f"오류가 발생했습니다: {e}")
