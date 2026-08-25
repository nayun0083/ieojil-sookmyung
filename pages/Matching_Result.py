import streamlit as st

from components.header import render_header
from components.footer import render_footer

from pages.algorithm import get_matching_result
from utils.auth import require_login, get_current_user
from utils.matching_result_db import (
    save_matching_result,
    get_latest_matching_result,
)
from utils.mentor_db import (
    get_mentors_by_type,
    get_active_mentor_profiles,
)
from utils.match_db import create_match_request


# =========================================
# 페이지 설정
# =========================================

st.set_page_config(
    page_title="매칭 결과 · 이어질 숙명",
    page_icon="💙",
    layout="wide"
)

render_header(active="test")
require_login()

user = get_current_user()


# =========================================
# 필수 질문
# =========================================

required_questions = [
    "q1",
    "q2",
    "q3",
    "q4",
    "q5",
]


# =========================================
# 답변 가져오기 / DB에서 불러오기 / 저장하기
# =========================================

answers = st.session_state.get("answers", {})


# 1. 방금 매칭 테스트를 완료하고 온 경우
if all(key in answers for key in required_questions):

    result = get_matching_result(answers)

    last_saved_answers = st.session_state.get(
        "last_saved_matching_answers"
    )

    # 같은 결과가 새로고침 때마다 중복 저장되지 않게 방지
    if last_saved_answers != answers:

        try:

            save_matching_result(
                mentee_id=user["id"],
                result=result,
                answers=answers,
            )

            st.session_state.last_saved_matching_answers = (
                answers.copy()
            )

        except Exception as e:

            st.warning(
                f"매칭 결과 저장 중 오류가 발생했습니다: {e}"
            )


# 2. 새로고침/재로그인해서 session_state에 answers가 없는 경우
else:

    try:

        latest_result = get_latest_matching_result(
            user["id"]
        )

    except Exception as e:

        st.error(
            f"저장된 매칭 결과를 불러오는 중 오류가 발생했습니다: {e}"
        )

        st.stop()


    if latest_result is None:

        st.warning(
            "먼저 매칭 테스트를 완료해주세요."
        )

        if st.button(
            "매칭 테스트 하러 가기",
            type="primary"
        ):

            st.session_state.q_index = 0
            st.session_state.force_new_matching_test = True

            st.switch_page(
                "pages/Matching_Test.py"
            )

        st.stop()


    # DB에 저장된 answers를 다시 session_state에 복구
    answers = latest_result.get("answers") or {}


    if not all(
        key in answers
        for key in required_questions
    ):

        st.warning(
            "저장된 매칭 결과가 올바르지 않습니다. "
            "매칭 테스트를 다시 진행해주세요."
        )

        if st.button(
            "매칭 테스트 다시 하기",
            type="primary"
        ):

            st.session_state.pop(
                "answers",
                None
            )

            st.session_state.pop(
                "result",
                None
            )

            st.session_state.pop(
                "last_saved_matching_answers",
                None
            )

            st.session_state.q_index = 0
            st.session_state.force_new_matching_test = True

            st.switch_page(
                "pages/Matching_Test.py"
            )

        st.stop()


    st.session_state.answers = answers

    st.session_state.last_saved_matching_answers = (
        answers.copy()
    )

    result = get_matching_result(
        answers
    )


# =========================================
# 결과 session_state 저장
# =========================================

st.session_state.result = result


# =========================================
# 최종 유형
# =========================================

st.markdown(
    f"# {result['emoji']} {result['type']}"
)

st.write(
    result["desc"]
)


# =========================================
# 유형 설명
# =========================================

with st.container(border=True):

    st.markdown(
        f"### {result['emoji']} {result['title']}"
    )

    st.write(
        result["desc"]
    )


st.divider()


# =========================================
# 유형별 점수
# =========================================

st.subheader(
    "📊 유형별 점수"
)


sorted_scores = sorted(
    result["scores"].items(),
    key=lambda x: x[1],
    reverse=True
)


emoji_map = {
    "열정송이": "🔥",
    "새싹송이": "🌱",
    "탐구송이": "🔍",
    "소통송이": "💬",
}


for type_name, score in sorted_scores:

    emoji = emoji_map[type_name]

    st.markdown(
        f"**{emoji} {type_name}** — "
        f"{score:.2f}점"
    )

    st.progress(
        min(score / 100, 1.0)
    )


st.divider()


# =========================================
# Q5 결과
# =========================================

st.subheader(
    "🕐 멘토링 가능 시간"
)

st.info(
    f"선택한 시간: **{answers['q5']}**"
)

st.caption(
    "Q5는 유형 분류에는 반영되지 않으며, "
    "추후 멘토·멘티 추천에 활용됩니다."
)


st.divider()


# =========================================
# 추천 멘토
# =========================================

st.subheader(
    "👩‍🎓 추천 멘토"
)

result_type = result["type"]


try:

    recommended_mentors = get_mentors_by_type(
        result_type
    )

except Exception as e:

    st.error(
        f"추천 멘토를 불러오는 중 오류가 발생했습니다: {e}"
    )

    recommended_mentors = []


if not recommended_mentors:

    st.warning(
        f"아직 {result_type} 유형에 등록된 멘토가 없어요."
    )

    with st.expander(
        "디버깅 정보 확인"
    ):

        try:

            all_mentors = get_active_mentor_profiles()

        except Exception as e:

            all_mentors = []

            st.error(
                f"전체 멘토 조회 오류: {e}"
            )

        st.write(
            "현재 매칭 결과 유형:",
            result_type
        )

        st.write(
            "DB에서 불러온 전체 멘토 수:",
            len(all_mentors)
        )

        st.write(
            "DB 멘토 목록:",
            all_mentors
        )


else:

    for mentor in recommended_mentors:

        mentor_id = mentor.get(
            "id"
        )

        mentor_name = mentor.get(
            "name",
            "이름 없음"
        )

        grade_text = str(
            mentor.get(
                "grade",
                "-"
            )
        )

        if grade_text.isdigit():

            grade_text = (
                f"{grade_text}학년"
            )


        with st.container(
            border=True
        ):

            st.markdown(
                f"### 👩‍🎓 {mentor_name}"
            )

            st.write(
                f"**학과:** {mentor.get('dept', '-')}"
            )

            st.write(
                f"**학년:** {grade_text}"
            )


            with st.expander(
                "추천 멘토 프로필 자세히 보기"
            ):

                st.write(
                    f"**이메일:** "
                    f"{mentor.get('email', '-')}"
                )

                st.write(
                    f"**도움 가능 분야:** "
                    f"{mentor.get('field', '-')}"
                )

                st.write(
                    f"**추천 후배 유형:** "
                    f"{mentor.get('type', '-')}"
                )

                st.write(
                    f"**가능 시간:** "
                    f"{mentor.get('available_time', '-')}"
                )

                st.write(
                    f"**한 줄 메시지:** "
                    f"{mentor.get('message', '-')}"
                )

                st.write("---")

                st.write(
                    mentor.get(
                        "intro",
                        ""
                    )
                )


            # =========================================
            # 매칭 신청 버튼
            # =========================================

            if st.button(
                "매칭 신청하기",
                type="primary",
                use_container_width=True,
                key=f"request_{mentor_id}"
            ):
                st.session_state.selected_mentor = mentor
                st.switch_page("pages/Mentoring_Request.py")

                    st.info(
                        "알림 페이지에서 신청 상태를 "
                        "확인할 수 있어요."
                    )

                    st.balloons()


                except Exception as e:

                    st.error(
                        f"매칭 신청 중 오류가 발생했습니다: {e}"
                    )


st.divider()


# =========================================
# 질문별 상세 점수
# =========================================

with st.expander(
    "🔎 질문별 점수 상세 보기"
):

    question_names = {

        "q1":
        "Q1. 현재 나의 고민(관심사)은?",

        "q2":
        "Q2. 어떤 멘토/멘티를 만나고 싶나요?",

        "q3":
        "Q3. 나의 성향은?",

        "q4":
        "Q4. 나에게 제일 중요한 것은?",
    }


    detail_scores = result[
        "detail_scores"
    ]


    for question_key in [
        "q1",
        "q2",
        "q3",
        "q4",
    ]:

        st.markdown(
            f"#### {question_names[question_key]}"
        )


        if question_key not in detail_scores:

            continue


        for type_name in [
            "열정송이",
            "새싹송이",
            "탐구송이",
            "소통송이",
        ]:

            data = detail_scores[
                question_key
            ][type_name]


            st.write(
                f"{type_name}: "
                f"원점수 {data['raw']}점 "
                f"→ 가중점수 "
                f"{data['weighted']:.2f}점"
            )


st.divider()


# =========================================
# 다시 테스트
# =========================================

if st.button(
    "↻ 다시 테스트하기",
    use_container_width=True
):

    st.session_state.pop(
        "answers",
        None
    )

    st.session_state.pop(
        "result",
        None
    )

    st.session_state.pop(
        "last_saved_matching_answers",
        None
    )

    st.session_state.pop(
        "selected_mentor",
        None
    )

    st.session_state.pop(
        "match_request",
        None
    )

    st.session_state.q_index = 0

    # 이 버튼을 눌렀을 때만
    # 기존 DB 결과가 있어도 새 테스트 시작
    st.session_state.force_new_matching_test = True

    st.switch_page(
        "pages/Matching_Test.py"
    )


render_footer()
