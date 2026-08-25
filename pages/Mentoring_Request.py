import streamlit as st
from datetime import date, time

from components.header import render_header
from components.footer import render_footer
from utils.auth import require_login, get_current_user
from utils.match_db import create_match_request


# =========================================
# 페이지 설정
# =========================================

st.set_page_config(
    page_title="멘토링 신청서 · 이어질 숙명",
    page_icon="💙",
    layout="wide"
)

render_header(active="test")
require_login()

user = get_current_user()

mentor = st.session_state.get("selected_mentor")
result = st.session_state.get("result", {})
answers = st.session_state.get("answers", {})


# =========================================
# 멘토 정보 없을 때
# =========================================

if not mentor:
    st.warning("신청할 멘토 정보가 없습니다. 매칭 결과 페이지에서 멘토를 다시 선택해주세요.")

    if st.button("매칭 결과로 돌아가기", type="primary"):
        st.switch_page("pages/Matching_Result.py")

    st.stop()


# =========================================
# 기본 데이터
# =========================================

core_worry = answers.get("q1", "-")
mentor_style = answers.get("q2", "-")
communication_style = answers.get("q3", "-")
core_value = answers.get("q4", "-")
preferred_time_from_test = answers.get("q5", "상관없음")

result_type = result.get("type", mentor.get("type", "-"))

name = user.get("name", "사용자")
dept = user.get("dept", user.get("department", "-"))
grade = user.get("grade", "-")
student_id = user.get("student_id", user.get("sid", ""))

grade_text = str(grade)
if grade_text.isdigit():
    grade_text = f"{grade_text}학년"

mentor_grade_text = str(mentor.get("grade", "-"))
if mentor_grade_text.isdigit():
    mentor_grade_text = f"{mentor_grade_text}학년"


# =========================================
# q1 답변에 따른 신청서 분기
# =========================================

is_major_or_career = (
    core_worry in [
        "전공·학업",
        "진로·취업",
        "전공 및 학업",
        "진로 및 취업",
    ]
)

is_campus_life = (
    core_worry in [
        "대학생활·인간관계",
        "대학생활 및 인간관계",
    ]
)

is_friendship = (
    "친해지고" in core_worry
    or "특별한 고민 없음" in core_worry
)


# =========================================
# 유틸 함수
# =========================================

def format_schedule(selected_date, selected_time):
    return f"{selected_date.month}/{selected_date.day} {selected_time.strftime('%H:%M')}"


# =========================================
# 화면 시작
# =========================================

st.title("멘토링 신청서")
st.caption("매칭 테스트 답변을 바탕으로 멘토에게 전달할 신청서를 작성해주세요.")

st.divider()


# =========================================
# 신청 멘토 정보
# =========================================

with st.container(border=True):
    st.subheader("👩‍🎓 신청할 멘토")

    st.markdown(f"### {mentor.get('name', '이름 없음')}")
    st.write(f"**학과:** {mentor.get('dept', '-')}")
    st.write(f"**학년:** {mentor_grade_text}")
    st.write(f"**도움 가능 분야:** {mentor.get('field', '-')}")
    st.write(f"**추천 후배 유형:** {mentor.get('type', '-')}")


st.divider()


# =========================================
# 매칭 테스트 기반 자동 연동 카드
# =========================================

with st.container(border=True):
    st.subheader("📌 멘티 프로필 요약")

    if student_id:
        st.write(f"**이름/닉네임:** {name} ({dept} / {grade_text} / {student_id})")
    else:
        st.write(f"**이름/닉네임:** {name} ({dept} / {grade_text})")

    st.write(f"**선택한 핵심 고민:** {core_worry}")
    st.write(f"**핵심 가치관:** {core_value}")
    st.write(f"**소통 성향:** {communication_style}")
    st.write(f"**원하는 멘토 스타일:** {mentor_style}")
    st.write(f"**기본 선호 시간대:** {preferred_time_from_test}")
    st.write(f"**매칭 유형:** {result_type}")


st.divider()


# =========================================
# 멘토링 신청서 작성
# =========================================

st.subheader("멘토링 세부 정보 입력")

with st.form("mentoring_request_form"):

    # -----------------------------------------
    # 전공·학업 / 진로·취업
    # -----------------------------------------
    if is_major_or_career:
        st.markdown("### 전공·학업 / 진로 관련 신청 내용")

        preferred_field = st.text_input(
            "세부 진로/관심 분야",
            placeholder="예: AI/데이터 진로, 웹 개발 공부, 대학원 준비, 학점 관리, 인턴·취업 준비 등"
        )

        question_1 = st.text_input(
            "핵심 질문 1",
            max_chars=100,
            placeholder="예: 2학년 2학기 학부 연구생 진입 시기와 필수 역량이 궁금합니다."
        )

        question_2 = st.text_input(
            "핵심 질문 2 선택",
            max_chars=100,
            placeholder="예: 포트폴리오를 준비할 때 프로젝트 규모와 기술 스택 중 무엇이 더 중요한가요?"
        )

        background = st.text_area(
            "현재 나의 배경/상황 선택",
            max_chars=200,
            placeholder="질문과 관련해 현재 준비 중이거나 겪고 있는 상황을 간단히 적어주세요.",
            height=120
        )

        selected_fields = []
        custom_field = ""

    # -----------------------------------------
    # 대학생활·인간관계
    # -----------------------------------------
    elif is_campus_life:
        st.markdown("### 대학생활 / 인간관계 관련 신청 내용")

        campus_options = [
            "동아리/소모임",
            "교환학생/어학연수",
            "대외활동/공모전",
            "선후배·동기 관계",
            "시간 관리/번아웃",
        ]

        selected_fields = st.multiselect(
            "궁금한 캠퍼스 영역",
            campus_options,
            help="궁금한 영역을 선택해주세요."
        )

        question_1 = st.text_input(
            "듣고 싶은 팁 및 핵심 질문 1",
            max_chars=100,
            placeholder="예: 학업과 동아리 활동을 병행하면서 학점 관리하는 노하우가 궁금해요."
        )

        question_2 = st.text_input(
            "듣고 싶은 팁 및 핵심 질문 2 선택",
            max_chars=100,
            placeholder="예: 대외활동을 처음 시작할 때 어떤 활동부터 하면 좋을까요?"
        )

        background = st.text_area(
            "현재 나의 고민 상황 선택",
            max_chars=200,
            placeholder="어떤 부분에서 어려움을 느끼고 있는지 편하게 공유해주세요.",
            height=120
        )

        preferred_field = ""
        custom_field = ""

    # -----------------------------------------
    # 특별한 고민 없음 / 친해지고 싶어요
    # -----------------------------------------
    else:
        st.markdown("### 친목 / 교류 관련 신청 내용")

        interest_options = [
            "#맛집탐방",
            "#음악/공연",
            "#운동/헬스",
            "#게임/e스포츠",
            "#영화/OTT",
            "#여행",
            "직접 입력",
        ]

        selected_fields = st.multiselect(
            "나의 관심사 & 취미 키워드",
            interest_options,
            help="최대 3개까지 선택해주세요."
        )

        custom_field = ""

        if "직접 입력" in selected_fields:
            custom_field = st.text_input(
                "직접 입력",
                placeholder="예: #카페투어, #뮤지컬, #독서"
            )

        question_1 = st.text_area(
            "멘토 선배와 나누고 싶은 이야기",
            max_chars=150,
            placeholder="예: 학교 앞 찐 맛집 추천받고 싶고, 편하게 대학 생활 썰 듣고 싶어서 신청했습니다 :)",
            height=120
        )

        question_2 = ""
        background = ""
        preferred_field = ""


    st.divider()


    # =========================================
    # 공통 영역. 진행 방식 및 일정 조율
    # =========================================

    st.subheader("멘토링 방식과 희망 일정")

    mentoring_method = st.radio(
        "희망 멘토링 방식",
        [
            "캠퍼스 대면 커피챗(카페/학교 라운지)",
            "온라인으로 이야기하기(Google Meet/디스코드)",
            "오픈채팅/이메일로 이야기하기",
        ]
    )

    st.markdown("#### 희망 일정 후보")

    col1, col2 = st.columns(2)

    with col1:
        date_1 = st.date_input(
            "1순위 날짜",
            value=date.today()
        )

        date_2 = st.date_input(
            "2순위 날짜",
            value=date.today()
        )

    with col2:
        time_1 = st.time_input(
            "1순위 시간",
            value=time(18, 0)
        )

        time_2 = st.time_input(
            "2순위 시간",
            value=time(19, 0)
        )

    weekend_flexible = st.checkbox("3순위: 주말 협의 가능")

    if not weekend_flexible:
        col3, col4 = st.columns(2)

        with col3:
            date_3 = st.date_input(
                "3순위 날짜",
                value=date.today()
            )

        with col4:
            time_3 = st.time_input(
                "3순위 시간",
                value=time(18, 0)
            )

    else:
        date_3 = None
        time_3 = None

    submitted = st.form_submit_button(
        "신청서 보내기",
        type="primary"
    )


# =========================================
# 제출 처리
# =========================================

if submitted:

    # -----------------------------------------
    # 전공·학업 / 진로·취업 검증
    # -----------------------------------------
    if is_major_or_career:
        if not preferred_field.strip():
            st.warning("세부 진로/관심 분야를 입력해주세요.")
            st.stop()

        preferred_field = preferred_field.strip()

    # -----------------------------------------
    # 대학생활 / 친목 검증
    # -----------------------------------------
    else:
        if not selected_fields:
            st.warning("세부 분야 또는 관심사를 최소 1개 이상 선택해주세요.")
            st.stop()

        if "직접 입력" in selected_fields and not custom_field.strip():
            st.warning("직접 입력 내용을 작성해주세요.")
            st.stop()

        if is_friendship and len(selected_fields) > 3:
            st.warning("관심사 & 취미 키워드는 최대 3개까지 선택해주세요.")
            st.stop()

        final_fields = [
            field for field in selected_fields
            if field != "직접 입력"
        ]

        if custom_field.strip():
            final_fields.append(custom_field.strip())

        preferred_field = " · ".join(final_fields)


    # -----------------------------------------
    # 공통 검증
    # -----------------------------------------
    if not question_1.strip():
        st.warning("필수 질문 또는 대화 주제를 입력해주세요.")
        st.stop()


    # -----------------------------------------
    # 일정 텍스트 만들기
    # -----------------------------------------
    schedule_1 = format_schedule(date_1, time_1)
    schedule_2 = format_schedule(date_2, time_2)

    if weekend_flexible:
        schedule_3 = "주말 협의 가능"
    else:
        schedule_3 = format_schedule(date_3, time_3)


    # -----------------------------------------
    # DB 저장용 텍스트 정리
    # -----------------------------------------
    topic = f"{core_worry} > {preferred_field}"

    full_question = f"""[멘티 프로필 요약]
이름/닉네임: {name}
전공/학년: {dept} / {grade_text}
선택한 핵심 고민: {core_worry}
핵심 가치관: {core_value}
소통 성향: {communication_style}
원하는 멘토 스타일: {mentor_style}
기본 선호 시간대: {preferred_time_from_test}
매칭 유형: {result_type}

[멘토링 세부 정보]
신청 분야: {core_worry}
세부 진로/관심 분야: {preferred_field}
핵심 질문 1: {question_1.strip()}
핵심 질문 2: {question_2.strip() if question_2 else "-"}
현재 상황: {background.strip() if background else "-"}

[멘토링 방식과 희망 일정]
희망 방식: {mentoring_method}
1순위: {schedule_1}
2순위: {schedule_2}
3순위: {schedule_3}
"""

    preferred_time = f"{mentoring_method} / 1순위: {schedule_1}"


    # -----------------------------------------
    # 신청서 저장
    # -----------------------------------------
    try:
        saved_request = create_match_request(
            mentor_id=mentor.get("user_id"),
            mentee_id=user.get("id"),
            mentor_profile_id=mentor.get("id"),
            result_type=result_type,
            topic=topic,
            preferred_time=preferred_time,
            question=full_question,
            preferred_field=preferred_field,

            mentor_name=mentor.get("name", ""),
            mentee_name=name,
            mentee_dept=dept,
            mentee_grade=grade_text,
            main_question=question_1.strip(),
            mentoring_method=mentoring_method,
            schedule_1=schedule_1,
            schedule_2=schedule_2,
            schedule_3=schedule_3,
        )

        st.session_state.match_request = saved_request

        st.success("멘토링 신청서가 전송되었습니다!")
        st.info("알림 페이지에서 신청 상태를 확인할 수 있어요.")

        if st.button("알림에서 확인하기", use_container_width=True):
            st.switch_page("pages/Notifications.py")

    except Exception as e:
        st.error(f"멘토링 신청서 전송 중 오류가 발생했습니다: {e}")


st.divider()

if st.button("매칭 결과로 돌아가기", use_container_width=True):
    st.switch_page("pages/Matching_Result.py")


render_footer()
