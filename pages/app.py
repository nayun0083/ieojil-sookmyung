import streamlit as st


# =========================================
# 페이지 기본 설정
# =========================================

st.set_page_config(
    page_title="이어질 숙명",
    page_icon="💙",
    layout="wide"
)


# =========================================
# 메인 화면
# =========================================

st.title("💙 이어질 숙명")

st.subheader("선후배 매칭 테스트")

st.write(
    "몇 가지 질문을 통해 나의 성향을 알아보고 "
    "나에게 맞는 송이 유형을 확인해보세요."
)

st.write("")


if st.button(
    "매칭 테스트 시작하기",
    type="primary",
    use_container_width=True
):
    st.switch_page(
        "pages/Matching_Test.py"
    )
