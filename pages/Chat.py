import streamlit as st
from datetime import datetime
from components.header import render_header
from components.footer import render_footer
from components.chat_message import render_message
from utils.auth import require_login, get_current_user

st.set_page_config(page_title="채팅 · 이어질 숙명",page_icon="💙", layout="wide")

render_header(active="chat")
require_login()

st.title("채팅")

user = get_current_user()
user_id = user.get("id")

if not user_id:
    st.error("사용자 정보를 불러올 수 없습니다. 다시 로그인해주세요.")
    st.stop()

match_request = st.session_state.get("match_request")

# 매칭 신청 자체가 없는 경우
if not match_request:
    with st.container(border=True):
        st.info("아직 생성된 채팅방이 없어요.")
        st.caption("매칭 테스트를 완료하고 선배에게 매칭을 신청해보세요.")

    if st.button("매칭 테스트 하러 가기", type="primary"):
        st.switch_page("pages/Matching_Test.py")

    render_footer()
    st.stop()

# 아직 수락되지 않은 경우
if match_request.get("status") != "accepted":
    mentor = match_request["mentor"]

    with st.container(border=True):
        st.warning("아직 매칭이 수락되지 않았어요.")
        st.write(f"**신청한 멘토:** {mentor['name']}")
        st.caption("선배가 매칭을 수락하면 채팅방이 열립니다.")

    if st.button("알림에서 상태 확인하기", type="primary"):
        st.switch_page("pages/Notifications.py")

    render_footer()
    st.stop()

mentor = match_request["mentor"]

st.session_state.setdefault("demo_messages", [])

if not st.session_state.demo_messages:
    st.session_state.demo_messages = [
        {
            "sender_id": "mentor_demo",
            "sender_name": mentor["name"],
            "content": "안녕하세요! 매칭 수락했어요 😊 궁금한 점 편하게 물어봐요.",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    ]

AI_TOPICS = [
    "선배님, 전공 수업 중 추천하는 과목이 있나요?",
    "대외활동은 어떻게 시작하는 게 좋을까요?",
    "진로 고민이 있는데 조언 부탁드려요!",
    "시간 괜찮으실 때 커피챗 가능할까요?",
]

col_list, col_topic, col_chat = st.columns([1, 1, 2])

# -----------------------------
# 왼쪽: 채팅 목록
# -----------------------------
with col_list:
    st.markdown("#### 채팅 목록")

    with st.container(border=True, height=520):
        st.button(
            f"👤 {mentor['name']}",
            type="primary",
            use_container_width=True,
            disabled=True,
        )

        st.caption("매칭이 완료된 선배와의 채팅방입니다.")

# -----------------------------
# 가운데: 추천 대화 주제
# -----------------------------
with col_topic:
    st.markdown("#### 추천 대화 주제")

    with st.container(border=True, height=520):
        st.caption("주제를 누르면 바로 메시지로 입력돼요.")

        for i, topic in enumerate(AI_TOPICS):
            if st.button(topic, key=f"topic_{i}", use_container_width=True):
                st.session_state.demo_messages.append(
                    {
                        "sender_id": user_id,
                        "sender_name": user.get("name", "나"),
                        "content": topic,
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                )

                # 데모용 자동 답장
                st.session_state.demo_messages.append(
                    {
                        "sender_id": "mentor_demo",
                        "sender_name": mentor["name"],
                        "content": "좋은 질문이에요! 제가 경험한 걸 바탕으로 차근차근 알려드릴게요 😊",
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                )

                st.rerun()

# -----------------------------
# 오른쪽: 채팅창
# -----------------------------
with col_chat:
    st.markdown(f"#### 💬 {mentor['name']} 선배와의 대화")

    with st.container(border=True, height=460):
        for msg in st.session_state.demo_messages:
            render_message(msg, user_id)

    prompt = st.chat_input("메시지를 입력하세요...")

    if prompt:
        st.session_state.demo_messages.append(
            {
                "sender_id": user_id,
                "sender_name": user.get("name", "나"),
                "content": prompt,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

        # 데모용 자동 답장
        st.session_state.demo_messages.append(
            {
                "sender_id": "mentor_demo",
                "sender_name": mentor["name"],
                "content": "응 좋아요! 그 부분은 이렇게 생각해보면 도움이 될 것 같아요 😊",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

        st.rerun()

st.divider()

if st.button("🧹 데모 채팅 초기화"):
    st.session_state.demo_messages = []
    st.rerun()

render_footer()