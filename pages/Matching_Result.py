import streamlit as st

from components.header import render_header
from components.footer import render_footer
from utils.matching import get_matching_result
from utils.auth import require_login, get_current_user
from utils.mentor_db import get_mentors_by_type, get_active_mentor_profiles
from utils.matching_result_db import save_matching_result, get_latest_matching_result


st.set_page_config(
    page_title="매칭 결과 · 이어질 숙명",
    page_icon="💙",
    layout="wide"
)

render_header(active="test")
require_login()

user = get_current_user()

TYPE_EMOJI = {
    "열정송이": "🔥",
    "새싹송이": "🌱",
    "탐구송이": "🔍",
    "소통송이": "💬",
}


# -----------------------------
# 매칭 결과 불러오기 / 저장하기
# -----------------------------
answers = st.session_state.get("answers", {})

if answers and "q4" in answers:
    # 방금 매칭 테스트를 완료하고 넘어온 경우
    result = get_matching_result(answers)

    # 같은 세션에서 새로고침/버튼 클릭으로 중복 저장되는 것 방지
    last_saved_answers = st.session_state.get("last_saved_matching_answers")

    if last_saved_answers != answers:
        try:
            saved_result = save_matching_result(
                mentee_id=user["id"],
                result=result,
                answers=answers,
            )
            st.session_state.latest_matching_result = saved_result
            st.session_state.last_saved_matching_answers = answers.copy()
        except Exception as e:
            st.warning(f"매칭 결과 저장 중 오류가 발생했습니다: {e}")

else:
    # 새로고침/재로그인 후 들어온 경우 DB에서 최근 결과 불러오기
    latest_result = get_latest_matching_result(user["id"])

    if latest_result is None:
        st.warning("먼저 매칭 테스트를 완료해주세요.")
        if st.button("매칭 테스트 하러 가기", type="primary"):
            st.switch_page("pages/Matching_Test.py")
        st.stop()

    result = {
        "type": latest_result.get("result_type"),
        "title": latest_result.get("title") or latest_result.get("result_type"),
        "desc": latest_result.get("description") or "",
        "scores": latest_result.get("scores") or {},
    }

    answers = latest_result.get("answers") or {}
    st.session_state.answers = answers

st.session_state.result = result

result_type = result.get("type")
emoji = TYPE_EMOJI.get(result_type, "🌸")


# -----------------------------
# 결과 화면
# -----------------------------
st.markdown(
    f"""
    <div style='text-align:center; padding:24px 0;'>
        <h1>{emoji} {result.get('title', '매칭 결과')}</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.container(border=True):
    st.markdown(f"### {emoji} {result_type}")
    st.write(result.get("desc", ""))

# 매칭 테스트 다시 하기 버튼
if st.button("매칭 테스트 다시 하기", use_container_width=True):
    st.session_state.pop("answers", None)
    st.session_state.pop("result", None)
    st.session_state.pop("selected_mentor", None)
    st.session_state.pop("match_request", None)
    st.session_state.pop("last_saved_matching_answers", None)
    st.switch_page("pages/Matching_Test.py")

st.divider()


# -----------------------------
# Supabase에서 추천 멘토 불러오기
# -----------------------------
st.subheader("👩‍🎓 추천 멘토")

try:
    recommended_mentors = get_mentors_by_type(result_type)
except Exception as e:
    st.error(f"추천 멘토를 불러오는 중 오류가 발생했습니다: {e}")
    recommended_mentors = []


if not recommended_mentors:
    st.warning(f"아직 {result_type} 유형에 등록된 멘토가 없어요.")

    with st.expander("디버깅 정보 확인"):
        try:
            all_mentors = get_active_mentor_profiles()
        except Exception as e:
            all_mentors = []
            st.error(f"전체 멘토 조회 오류: {e}")

        st.write("현재 매칭 결과 유형:", result_type)
        st.write("DB에서 불러온 전체 멘토 수:", len(all_mentors))
        st.write("DB 멘토 목록:", all_mentors)

else:
    for mentor in recommended_mentors:
        mentor_id = mentor.get("id")
        mentor_name = mentor.get("name", "이름 없음")

        grade_text = str(mentor.get("grade", "-"))
        if grade_text.isdigit():
            grade_text = f"{grade_text}학년"

        with st.container(border=True):
            # 기본 카드에는 핵심 정보만 보여주기
            st.markdown(f"### 👩‍🎓 {mentor_name}")
            st.write(f"**학과:** {mentor.get('dept', '-')}")
            st.write(f"**학년:** {grade_text}")

            # 자세한 정보는 expander 안으로 넣기
            with st.expander("추천 멘토 프로필 자세히 보기"):
                st.write(f"**이메일:** {mentor.get('email', '-')}")
                st.write(f"**도움 가능 분야:** {mentor.get('field', '-')}")
                st.write(f"**추천 후배 유형:** {mentor.get('type', '-')}")
                st.write(f"**가능 시간:** {mentor.get('available_time', '-')}")
                st.write(f"**한 줄 메시지:** {mentor.get('message', '-')}")
                st.write("---")
                st.write(mentor.get("intro", ""))

            match_request = st.session_state.get("match_request")

            already_requested = (
                match_request is not None
                and match_request.get("mentor", {}).get("id") == mentor_id
            )

            if already_requested:
                status = match_request.get("status", "pending")

                if status == "pending":
                    st.info("이미 이 선배에게 매칭을 신청했어요. 수락을 기다리는 중입니다.")
                elif status == "accepted":
                    st.success("이 선배와 매칭이 수락되었어요! 채팅을 시작할 수 있습니다.")
                else:
                    st.warning("이 매칭 신청은 처리되었습니다.")

            else:
                if st.button(
                    "매칭 신청하기",
                    type="primary",
                    use_container_width=True,
                    key=f"request_{mentor_id}"
                ):
                    st.session_state.selected_mentor = mentor

                    st.session_state.match_request = {
                        "mentor": mentor,
                        "mentor_profile_id": mentor.get("id"),
                        "mentor_id": mentor.get("user_id"),
                        "result_type": result_type,
                        "status": "pending",
                        "mentee": {
                            "id": user.get("id"),
                            "name": user.get("name", "사용자"),
                            "email": user.get("email", ""),
                            "dept": user.get("dept", ""),
                            "grade": user.get("grade", ""),
                        },
                    }

                    st.success(f"{mentor_name}에게 매칭을 신청했어요!")
                    st.info("알림 페이지에서 신청 상태를 확인할 수 있어요.")
                    st.balloons()

st.divider()


# -----------------------------
# 알림 페이지 이동
# -----------------------------
if st.button("알림에서 상태 확인하기", use_container_width=True):
    st.switch_page("pages/Notifications.py")


st.divider()


# -----------------------------
# 점수 상세 보기
# -----------------------------
with st.expander("유형별 점수 상세 보기"):
    scores = result.get("scores", {})
    for type_name, score in scores.items():
        st.markdown(f"- **{type_name}**: {score}점")


render_footer()
