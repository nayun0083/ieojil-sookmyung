import streamlit as st
from components.header import render_header
from components.footer import render_footer
from utils.auth import require_login

st.set_page_config(page_title="매칭 테스트 · 이어질 숙명", page_icon="💙", layout="wide")

render_header(active="test")
require_login()   # 미로그인 시 여기서 차단 + 로그인 페이지 안내

st.session_state.setdefault("answers", {})
st.session_state.setdefault("q_index", 0)

# 질문 정의 (한 문항씩 진행)
QUESTIONS = [
    {"key": "q1", "type": "radio", "q": "Q1. 어떤 도움을 받고 싶나요?",
     "options": ["학교생활", "전공", "취업", "대외활동"]},
    {"key": "q1_1", "type": "text", "q": "Q1-1. 현재 가장 고민되는 것은 무엇인가요?",
     "placeholder": "예: 진로가 고민돼요 / 친구 관계 / 전공 공부 등"},
    {"key": "q2", "type": "radio", "q": "Q2. 관심 분야는 무엇인가요?",
     "options": ["AI", "웹개발", "앱개발", "디자인"]},
    {"key": "q3", "type": "radio", "q": "Q3. 어떤 선배를 만나고 싶나요?",
     "options": ["친절한", "친구 같은", "경험 많은", "꼼꼼한"]},
    {"key": "q4", "type": "radio", "q": "Q4. 나의 성향은?",
     "options": ["도전형", "계획형", "신중형", "사교형"]},
    {"key": "q5", "type": "radio", "q": "Q5. 멘토링 가능한 시간은?",
     "options": ["평일", "주말", "저녁", "상관없음"]},
]

idx = st.session_state.q_index
total = len(QUESTIONS)

st.title("매칭 테스트")
st.progress((idx) / total, text=f"{idx}/{total} 완료")

if idx < total:
    q = QUESTIONS[idx]
    with st.container(border=True):
        st.subheader(q["q"])
        if q["type"] == "radio":
            ans = st.radio("선택하세요", q["options"], key=f"input_{q['key']}",
                           label_visibility="collapsed")
        else:
            ans = st.text_input("입력하세요", key=f"input_{q['key']}",
                                placeholder=q.get("placeholder", ""),
                                label_visibility="collapsed")

    col1, col2 = st.columns(2)
    with col1:
        if idx > 0 and st.button("⬅ 이전", use_container_width=True):
            st.session_state.q_index -= 1
            st.rerun()
    with col2:
        label = "결과 보기 " if idx == total - 1 else "다음 ➡"
        if st.button(label, type="primary", use_container_width=True):
            if q["type"] == "text" and not ans.strip():
                st.warning("고민 내용을 입력해주세요.")
            else:
                st.session_state.answers[q["key"]] = ans
                st.session_state.q_index += 1
                st.rerun()
else:
    st.success("모든 질문에 답했어요! 결과를 확인하세요.")
    if st.button("결과 보기", type="primary", use_container_width=True):
        st.switch_page("pages/Matching_Result.py")  # 결과 보기

    if st.button("다시 테스트하기", use_container_width=True):
        st.session_state.q_index = 0
        st.session_state.answers = {}
        st.rerun()

render_footer()
