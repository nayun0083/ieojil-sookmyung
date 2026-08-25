import streamlit as st

from pages.algorithm import (
    SCORING_TABLE,
    TIME_OPTIONS
)


# =========================================
# 페이지 설정
# =========================================

st.set_page_config(
    page_title="매칭 테스트 · 이어질 숙명",
    page_icon="💙",
    layout="wide"
)


# =========================================
# 세션 상태 초기화
# =========================================

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "q_index" not in st.session_state:
    st.session_state.q_index = 0


# =========================================
# 질문 정의
# =========================================

QUESTIONS = [

    {
        "key": "q1",
        "question": "Q1. 현재 나의 고민(관심사)은?",
        "options": list(SCORING_TABLE["q1"].keys()),
    },

    {
        "key": "q2",
        "question": "Q2. 어떤 멘토/멘티를 만나고 싶나요?",
        "options": list(SCORING_TABLE["q2"].keys()),
    },

    {
        "key": "q3",
        "question": "Q3. 나의 성향은?",
        "options": list(SCORING_TABLE["q3"].keys()),
    },

    {
        "key": "q4",
        "question": "Q4. 나에게 제일 중요한 것은?",
        "options": list(SCORING_TABLE["q4"].keys()),
    },

    {
        "key": "q5",
        "question": "Q5. 멘토링이 가장 편한 시간은?",
        "options": TIME_OPTIONS,
    },
]


# =========================================
# 현재 질문
# =========================================

idx = st.session_state.q_index
total = len(QUESTIONS)


# =========================================
# 제목
# =========================================

st.title("💙 매칭 테스트")

st.write(
    "각 질문에 가장 가까운 답변을 선택해주세요."
)


# =========================================
# 진행률
# =========================================

st.progress(
    idx / total,
    text=f"{idx}/{total} 완료"
)


# =========================================
# 질문 출력
# =========================================

if idx < total:

    q = QUESTIONS[idx]

    with st.container(border=True):

        st.subheader(q["question"])

        current_answer = st.session_state.answers.get(
            q["key"]
        )

        if current_answer in q["options"]:
            default_index = q["options"].index(
                current_answer
            )
        else:
            default_index = None

        answer = st.radio(
            "선택해주세요",
            q["options"],
            index=default_index,
            key=f"input_{q['key']}",
            label_visibility="collapsed"
        )

        st.write("")

        col1, col2 = st.columns(2)

        # =====================================
        # 이전 버튼
        # =====================================

        with col1:

            if idx > 0:

                if st.button(
                    "⬅ 이전",
                    use_container_width=True
                ):

                    st.session_state.answers[
                        q["key"]
                    ] = answer

                    st.session_state.q_index -= 1

                    st.rerun()


        # =====================================
        # 다음 / 결과 버튼
        # =====================================

        with col2:

            if idx == total - 1:
                button_text = "결과 보기 🎉"
            else:
                button_text = "다음 ➡"

            if st.button(
                button_text,
                type="primary",
                use_container_width=True
            ):

                st.session_state.answers[
                    q["key"]
                ] = answer

                if idx == total - 1:

                    st.switch_page(
                        "pages/Matching_Result.py"
                    )

                else:

                    st.session_state.q_index += 1

                    st.rerun()
