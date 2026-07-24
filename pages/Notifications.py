import streamlit as st

from components.header import render_header
from components.footer import render_footer
from utils.auth import require_login, get_current_user

st.set_page_config(
    page_title="알림 · 이어질 숙명",
    layout="wide",
    page_icon="💙"
)

render_header(active="noti")
require_login()

user = get_current_user()

st.title("알림")
st.caption("매칭 신청 현황과 받은 요청을 확인할 수 있어요.")

st.divider()

st.session_state.setdefault("match_request", None)
st.session_state.setdefault("demo_messages", [])
st.session_state.setdefault("incoming_requests", [])
st.session_state.setdefault("mentor_profile", None)

tab1, tab2 = st.tabs(["내 신청 현황", "받은 신청"])


# -----------------------------
# 내 신청 현황
# -----------------------------
with tab1:
    st.subheader("내가 보낸 매칭 신청")

    request = st.session_state.get("match_request")

    if not request:
        with st.container(border=True):
            st.info("아직 보낸 매칭 신청이 없습니다.")
            st.write("멘토를 선택해 매칭을 신청하면 이곳에서 상태를 확인할 수 있어요.")

        if st.button("홈으로 돌아가기", use_container_width=True):
            st.switch_page("app.py")

    else:
        mentor = request.get("mentor", {})
        status = request.get("status", "pending")

        with st.container(border=True):
            st.markdown(f"### 👩‍🎓 {mentor.get('name', '멘토')}")
            st.write(f"**학과:** {mentor.get('dept', '-')}")
            st.write(f"**관심 분야:** {mentor.get('field', '-')}")
            st.write(f"**추천 유형:** {mentor.get('type', request.get('result_type', '-'))}")

            if status == "pending":
                st.warning("현재 상태: 수락 대기 중")
                st.write("멘토가 신청을 확인하면 수락 여부가 표시됩니다.")

                c1, c2 = st.columns(2)

                with c1:
                    if st.button("신청 취소하기", use_container_width=True):
                        st.session_state.match_request = None
                        st.success("매칭 신청을 취소했습니다.")
                        st.rerun()

                with c2:
                    if st.button("데모용 수락 처리", use_container_width=True):
                        st.session_state.match_request["status"] = "accepted"
                        st.session_state.demo_messages = [
                            {
                                "sender_id": "mentor",
                                "sender_name": mentor.get("name", "멘토"),
                                "content": "안녕하세요! 매칭을 수락했어요. 편하게 질문해주세요 😊",
                                "created_at": "2026-07-25 10:00",
                            }
                        ]
                        st.success("매칭이 수락된 것으로 처리되었습니다.")
                        st.rerun()

            elif status == "accepted":
                st.success("현재 상태: 매칭 수락 완료")
                st.write("이제 채팅을 시작할 수 있어요.")

                if st.button("채팅 시작하기", type="primary", use_container_width=True):
                    st.switch_page("pages/Chat.py")

            elif status == "rejected":
                st.error("현재 상태: 매칭 거절")
                st.write("다른 멘토에게 다시 신청할 수 있어요.")

        if st.button("홈으로 돌아가기", use_container_width=True):
            st.switch_page("app.py")


# -----------------------------
# 받은 신청
# -----------------------------
with tab2:
    st.subheader("내게 온 매칭 신청")

    mentor_profile = st.session_state.get("mentor_profile")
    incoming_requests = st.session_state.get("incoming_requests", [])

    if not mentor_profile:
        with st.container(border=True):
            st.info("멘토 등록을 하면 후배들의 매칭 신청을 받을 수 있어요.")

        if st.button("멘토 등록하기", type="primary", use_container_width=True):
            st.switch_page("pages/Mentor_Register.py")

    else:
        with st.container(border=True):
            st.write("현재 멘토로 등록되어 있어요.")
            st.write(f"**멘토명:** {mentor_profile.get('name', '-')}")
            st.write(f"**도움 가능 분야:** {mentor_profile.get('field', '-')}")
            st.write(f"**추천 후배 유형:** {mentor_profile.get('type', '-')}")

        st.write("")

        if not incoming_requests:
            with st.container(border=True):
                st.info("아직 받은 매칭 신청이 없습니다.")
                st.write("후배가 매칭을 신청하면 이곳에서 수락하거나 거절할 수 있어요.")

        else:
            for idx, req in enumerate(incoming_requests):
                with st.container(border=True):
                    mentee = req.get("mentee", {})
                    st.markdown(f"### 🙋‍♀️ {mentee.get('name', '후배')}")
                    st.write(f"**학과:** {mentee.get('dept', '-')}")
                    st.write(f"**유형:** {req.get('result_type', '-')}")
                    st.write(f"**상태:** {req.get('status', 'pending')}")

                    c1, c2 = st.columns(2)

                    with c1:
                        if st.button("수락하기", key=f"accept_{idx}", use_container_width=True):
                            st.session_state.incoming_requests[idx]["status"] = "accepted"
                            st.success("매칭 신청을 수락했습니다.")
                            st.rerun()

                    with c2:
                        if st.button("거절하기", key=f"reject_{idx}", use_container_width=True):
                            st.session_state.incoming_requests[idx]["status"] = "rejected"
                            st.warning("매칭 신청을 거절했습니다.")
                            st.rerun()

render_footer()