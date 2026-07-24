import streamlit as st
from components.header import render_header
from components.footer import render_footer
from components.cards import mentor_card
from utils.matching import get_matching_result
from utils.auth import require_login, get_current_user

st.set_page_config(page_title="매칭 결과 · 이어질 숙명",page_icon="💙",  layout="wide")

render_header(active="test")
require_login()

answers = st.session_state.get("answers", {})

if not answers or "q4" not in answers:
    st.warning("먼저 매칭 테스트를 완료해주세요.")
    if st.button("매칭 테스트 하러 가기", type="primary"):
        st.switch_page("pages/Matching_Test.py")
    st.stop()

result = get_matching_result(answers)
st.session_state.result = result
st.session_state.selected_mentor = result["mentor"]

user = get_current_user()

TYPE_EMOJI = {
    "열정송이": "🔥",
    "새싹송이": "🌱",
    "탐구송이": "🔍",
    "소통송이": "💬",
}

emoji = TYPE_EMOJI.get(result["type"], "🌸")

st.markdown(
    f"""
    <div style='text-align:center; padding:24px 0;'>
        <h1>{emoji} {result['title']}</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.container(border=True):
    st.markdown(f"### {emoji} {result['type']}")
    st.write(result["desc"])

st.divider()

st.subheader("👩‍🎓 추천 멘토")
mentor = result["mentor"]
mentor_card(mentor)

with st.expander("추천 멘토 프로필 자세히 보기"):
    st.markdown(f"### {mentor['name']}")
    st.write(f"**학과:** {mentor['dept']}")
    st.write(f"**학번:** {mentor['sid']}")
    st.write(f"**관심 분야:** {mentor['field']}")
    st.write("---")
    st.write(
        "안녕하세요! 후배들의 학교생활과 진로 고민에 도움이 되고 싶은 선배입니다. "
        "편하게 질문하고 함께 방향을 찾아가요 😊"
    )

st.divider()

# 현재 매칭 신청 상태 확인
match_request = st.session_state.get("match_request")

already_requested = (
    match_request is not None
    and match_request.get("mentor", {}).get("name") == mentor["name"]
)

c1, c2 = st.columns(2)

with c1:
    if already_requested:
        status = match_request.get("status", "pending")

        if status == "pending":
            st.info("이미 이 선배에게 매칭을 신청했어요. 수락을 기다리는 중입니다.")
        elif status == "accepted":
            st.success("이 선배와 매칭이 수락되었어요! 채팅을 시작할 수 있습니다.")
        else:
            st.warning("이 매칭 신청은 처리되었습니다.")

    else:
        if st.button("매칭 신청하기", type="primary", use_container_width=True):
            st.session_state.match_request = {
                "mentor": mentor,
                "result_type": result["type"],
                "status": "pending",
                "mentee": {
                    "id": user.get("id"),
                    "name": user.get("name", "사용자"),
                    "email": user.get("email", ""),
                    "dept": user.get("dept", ""),
                    "grade": user.get("grade", ""),
                },
            }

            st.success(f"{mentor['name']}에게 매칭을 신청했어요!")
            st.info("알림 페이지에서 신청 상태를 확인할 수 있어요.")
            st.balloons()

with c2:
    if st.button("알림에서 상태 확인하기", use_container_width=True):
        st.switch_page("pages/Notifications.py")

st.divider()

with st.expander("유형별 점수 상세 보기"):
    scores = result.get("scores", {})
    for type_name, score in scores.items():
        st.markdown(f"- **{type_name}**: {score}점")

render_footer()