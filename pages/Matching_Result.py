import streamlit as st

from pages.algorithm import get_matching_result
from utils.auth import require_login, get_current_user
from utils.matching_result_db import save_matching_result, get_latest_matching_result


# =========================================
# 페이지 설정
# =========================================

st.set_page_config(
    page_title="매칭 결과 · 이어질 숙명",
    page_icon="💙",
    layout="wide"
)

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

    # 같은 결과가 새로고침 때마다 중복 저장되지 않게 방지
    last_saved_answers = st.session_state.get("last_saved_matching_answers")

    if last_saved_answers != answers:
        try:
            save_matching_result(
                mentee_id=user["id"],
                result=result,
                answers=answers,
            )

            st.session_state.last_saved_matching_answers = answers.copy()

        except Exception as e:
            st.warning(f"매칭 결과 저장 중 오류가 발생했습니다: {e}")

# 2. 새로고침/재로그인해서 session_state에 answers가 없는 경우
else:
    latest_result = get_latest_matching_result(user["id"])

    if latest_result is None:
        st.warning("먼저 매칭 테스트를 완료해주세요.")

        if st.button(
            "매칭 테스트 하러 가기",
            type="primary"
        ):
            st.session_state.q_index = 0
            st.switch_page("pages/Matching_Test.py")

        st.stop()

    # DB에 저장된 answers를 다시 session_state에 복구
    answers = latest_result.get("answers") or {}

    if not all(key in answers for key in required_questions):
        st.warning("저장된 매칭 결과가 올바르지 않습니다. 매칭 테스트를 다시 진행해주세요.")

        if st.button(
            "매칭 테스트 다시 하기",
            type="primary"
        ):
            st.session_state.answers = {}
            st.session_state.q_index = 0
            st.switch_page("pages/Matching_Test.py")

        st.stop()

    st.session_state.answers = answers

    # answers를 기반으로 다시 결과 계산
    result = get_matching_result(answers)


# 결과 session_state 저장
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

    st.session_state.pop("answers", None)
    st.session_state.pop("result", None)
    st.session_state.pop("last_saved_matching_answers", None)

    st.session_state.q_index = 0

    st.switch_page(
        "pages/Matching_Test.py"
    )
