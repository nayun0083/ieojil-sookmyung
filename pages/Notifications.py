import streamlit as st

from components.header import render_header
from components.footer import render_footer
from utils.auth import require_login, get_current_user

from utils.match_db import (
    get_sent_matches,
    get_received_matches,
    update_match_status,
)


st.set_page_config(
    page_title="알림 · 이어질 숙명",
    layout="wide",
    page_icon="💙"
)


# =========================================================
# 기본 설정
# =========================================================

render_header(active="noti")
require_login()

user = get_current_user()

st.title("알림")
st.caption("매칭 신청 현황과 받은 요청을 확인할 수 있어요.")

st.divider()


# =========================================================
# 현재 로그인한 사용자 ID
# =========================================================

if not user:
    st.error("로그인 정보를 찾을 수 없습니다.")
    st.stop()


user_id = user.get("id") if isinstance(user, dict) else user.id


# =========================================================
# 탭
# =========================================================

tab1, tab2 = st.tabs(["내 신청 현황", "받은 신청"])


# =========================================================
# 1. 내가 보낸 신청
# =========================================================

with tab1:

    st.subheader("내가 보낸 매칭 신청")

    try:
        sent_matches = get_sent_matches(user_id)

    except Exception as e:
        st.error(f"매칭 신청을 불러오는 중 오류가 발생했습니다: {e}")
        sent_matches = []


    if not sent_matches:

        with st.container(border=True):

            st.info("아직 보낸 매칭 신청이 없습니다.")

            st.write(
                "멘토를 선택해 매칭을 신청하면 "
                "이곳에서 상태를 확인할 수 있어요."
            )

        if st.button(
            "홈으로 돌아가기",
            use_container_width=True
        ):
            st.switch_page("app.py")


    else:

        for match in sent_matches:

            mentor_id = match.get("mentor_id", "-")
            status = match.get("status", "pending")

            # DB에 저장된 정보
            result_type = match.get("result_type", "-")
            topic = match.get("topic", "-")
            preferred_time = match.get("preferred_time", "-")
            preferred_field = match.get("preferred_field", "-")


            with st.container(border=True):

                st.markdown("### 👩‍🎓 매칭 신청")

                st.write(
                    f"**멘토 ID:** {mentor_id}"
                )

                st.write(
                    f"**희망 분야:** {preferred_field}"
                )

                st.write(
                    f"**주제:** {topic}"
                )

                st.write(
                    f"**선호 시간:** {preferred_time}"
                )

                st.write(
                    f"**추천 유형:** {result_type}"
                )


                # -----------------------------
                # 상태 표시
                # -----------------------------

                if status == "pending":

                    st.warning(
                        "현재 상태: 수락 대기 중"
                    )

                    st.write(
                        "멘토가 신청을 확인하면 "
                        "수락 여부가 표시됩니다."
                    )


                elif status == "accepted":

                    st.success(
                        "현재 상태: 매칭 수락 완료"
                    )

                    st.write(
                        "멘토가 매칭 신청을 수락했습니다."
                    )

                    if st.button(
                        "채팅 시작하기",
                        type="primary",
                        use_container_width=True,
                        key=f"chat_{match.get('id')}"
                    ):
                        st.switch_page("pages/Chat.py")


                elif status == "rejected":

                    st.error(
                        "현재 상태: 매칭 거절"
                    )

                    st.write(
                        "멘토가 매칭 신청을 거절했습니다. "
                        "다른 멘토에게 다시 신청할 수 있어요."
                    )


                else:

                    st.info(
                        f"현재 상태: {status}"
                    )


        if st.button(
            "홈으로 돌아가기",
            use_container_width=True,
            key="home_sent"
        ):
            st.switch_page("app.py")


# =========================================================
# 2. 내가 받은 신청
# =========================================================

with tab2:

    st.subheader("내게 온 매칭 신청")


    try:
        received_matches = get_received_matches(user_id)

    except Exception as e:
        st.error(
            f"받은 매칭 신청을 불러오는 중 오류가 발생했습니다: {e}"
        )
        received_matches = []


    if not received_matches:

        with st.container(border=True):

            st.info("아직 받은 매칭 신청이 없습니다.")

            st.write(
                "후배가 매칭을 신청하면 "
                "이곳에서 수락하거나 거절할 수 있어요."
            )


    else:

        for match in received_matches:

            match_id = match.get("id")
            mentee_id = match.get("mentee_id")
            status = match.get("status", "pending")

            result_type = match.get("result_type", "-")
            topic = match.get("topic", "-")
            preferred_time = match.get("preferred_time", "-")
            preferred_field = match.get("preferred_field", "-")
            mentee_intro = match.get("mentee_intro", "-")


            with st.container(border=True):

                st.markdown("### 🙋‍♀️ 매칭 신청")

                st.write(
                    f"**멘티 ID:** {mentee_id}"
                )

                st.write(
                    f"**희망 분야:** {preferred_field}"
                )

                st.write(
                    f"**주제:** {topic}"
                )

                st.write(
                    f"**선호 시간:** {preferred_time}"
                )

                st.write(
                    f"**추천 유형:** {result_type}"
                )

                st.write(
                    f"**멘티 소개:** {mentee_intro}"
                )


                # =========================================
                # pending
                # =========================================

                if status == "pending":

                    st.warning(
                        "현재 상태: 수락 대기 중"
                    )

                    c1, c2 = st.columns(2)


                    # -----------------------------
                    # 수락
                    # -----------------------------

                    with c1:

                        if st.button(
                            "✅ 수락하기",
                            key=f"accept_{match_id}",
                            use_container_width=True
                        ):

                            try:

                                update_match_status(
                                    match_id,
                                    "accepted"
                                )

                                st.success(
                                    "매칭 신청을 수락했습니다."
                                )

                                st.rerun()

                            except Exception as e:

                                st.error(
                                    f"수락 처리 중 오류가 발생했습니다: {e}"
                                )


                    # -----------------------------
                    # 거절
                    # -----------------------------

                    with c2:

                        if st.button(
                            "❌ 거절하기",
                            key=f"reject_{match_id}",
                            use_container_width=True
                        ):

                            try:

                                update_match_status(
                                    match_id,
                                    "rejected"
                                )

                                st.warning(
                                    "매칭 신청을 거절했습니다."
                                )

                                st.rerun()

                            except Exception as e:

                                st.error(
                                    f"거절 처리 중 오류가 발생했습니다: {e}"
                                )


                # =========================================
                # accepted
                # =========================================

                elif status == "accepted":

                    st.success(
                        "🟢 현재 상태: 수락 완료"
                    )


                # =========================================
                # rejected
                # =========================================

                elif status == "rejected":

                    st.error(
                        "🔴 현재 상태: 거절됨"
                    )


                st.divider()


render_footer()
