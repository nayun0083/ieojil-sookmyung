import streamlit as st

from components.header import render_header
from components.footer import render_footer
from utils.auth import require_login, get_current_user
from utils.supabase_client import get_client
from utils.mentor_db import save_mentor_profile, get_mentor_profile_by_user


st.set_page_config(
    page_title="멘토 등록 · 이어질 숙명",
    page_icon="💙",
    layout="wide"
)

render_header(active="mentor")
require_login()


# -----------------------------
# 사용자 정보 불러오기
# -----------------------------
def load_profile_user(user: dict) -> dict:
    """
    session_state에 저장된 user 정보가 부족할 수 있어서
    Supabase profiles 테이블에서 한 번 더 가져오기
    """
    if not user:
        return {}

    profile = dict(user)

    try:
        sb = get_client()

        user_id = profile.get("id")
        email = profile.get("email")

        if user_id:
            res = (
                sb.table("profiles")
                .select("*")
                .eq("id", user_id)
                .execute()
            )
        elif email:
            res = (
                sb.table("profiles")
                .select("*")
                .eq("email", email)
                .execute()
            )
        else:
            return profile

        if res.data and len(res.data) > 0:
            profile.update(res.data[0])

    except Exception:
        # profiles 조회가 실패해도 페이지가 멈추지 않도록 처리
        pass

    return profile


def clean_name(user: dict) -> str:
    """
    이름 칸에 이메일이 들어가는 경우 방지
    """
    name = str(user.get("name", "")).strip()
    email = str(user.get("email", "")).strip()

    if name and "@" not in name and name.lower() != email.lower():
        return name

    return ""


user = get_current_user()
user = load_profile_user(user)

display_name = clean_name(user)
display_dept = user.get("dept") or user.get("department") or ""
display_grade = user.get("grade") or ""
display_email = user.get("email") or ""


# -----------------------------
# 후배 유형 설명
# -----------------------------
TYPE_DESCRIPTIONS = {
    "새싹송이": "학교생활 적응, 수강신청, 전공 입문처럼 처음 시작하는 후배에게 잘 맞아요.",
    "탐구송이": "전공 공부, 개발, AI, 데이터 분석처럼 깊이 있게 배우고 싶은 후배에게 잘 맞아요.",
    "열정송이": "진로, 프로젝트, 대외활동처럼 목표를 가지고 도전하려는 후배에게 잘 맞아요.",
    "소통송이": "편안한 대화, 고민 상담, 학교생활 조언처럼 공감과 소통이 필요한 후배에게 잘 맞아요.",
}


# -----------------------------
# 세션 초기화
# -----------------------------
st.session_state.setdefault("mentor_profile", None)
st.session_state.setdefault("mentor_profiles", [])

# -----------------------------
# DB에 저장된 기존 멘토 정보 불러오기
# -----------------------------
existing_mentor_profile = None

if user.get("id"):
    existing_mentor_profile = get_mentor_profile_by_user(user["id"])

if existing_mentor_profile:
    existing_mentor_profile["type_description"] = TYPE_DESCRIPTIONS.get(
        existing_mentor_profile.get("type"),
        ""
    )
    st.session_state.mentor_profile = existing_mentor_profile

# -----------------------------
# 화면 시작
# -----------------------------
st.title("멘토 등록")
st.caption("후배들에게 어떤 도움을 줄 수 있는지 입력해주세요.")

st.divider()


# -----------------------------
# 이미 등록한 정보 보여주기
# -----------------------------
if st.session_state.mentor_profile:
    st.info("이미 등록된 멘토 정보가 있어요. 아래에서 수정할 수 있습니다.")

    profile = st.session_state.mentor_profile

    with st.container(border=True):
        st.subheader("현재 등록된 멘토 정보")
        st.write(f"**이름:** {profile.get('name', '-')}")
        st.write(f"**학과:** {profile.get('dept', '-')}")
        st.write(f"**학년:** {profile.get('grade', '-')}")
        st.write(f"**도움 가능 분야:** {profile.get('field', '-')}")
        st.write(f"**추천 후배 유형:** {profile.get('type', '-')}")
        st.write(f"**가능 시간:** {profile.get('available_time', '-')}")
        st.write(f"**한 줄 메시지:** {profile.get('message', '-')}")


# -----------------------------
# 멘토 등록 폼
# -----------------------------
st.subheader("멘토 정보 입력")

with st.form("mentor_register_form"):
    st.markdown("#### 기본 정보")
    st.caption("회원가입 때 입력한 정보가 자동으로 들어옵니다. 잘못 보이면 이 화면에서 수정할 수 있어요.")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input(
            "이름",
            value=display_name,
            placeholder="예: 김숙명"
        )

        dept = st.text_input(
            "학과",
            value=display_dept,
            placeholder="예: 데이터사이언스학과"
        )

    with col2:
        grade = st.text_input(
            "학년",
            value=display_grade,
            placeholder="예: 2학년"
        )

        email = st.text_input(
            "학교 이메일",
            value=display_email,
            disabled=True
        )

    st.markdown("#### 멘토 활동 정보")

    help_fields = st.multiselect(
        "도움 가능 분야",
        [
            "학교생활",
            "수강신청",
            "전공 공부",
            "진로 고민",
            "대외활동",
            "프로젝트",
            "개발 공부",
            "고민 상담",
        ],
        help="후배에게 도움을 줄 수 있는 분야를 선택해주세요."
    )

    mentor_type = st.selectbox(
        "어떤 유형의 후배와 잘 맞나요?",
        list(TYPE_DESCRIPTIONS.keys())
    )

    with st.container(border=True):
        st.markdown(f"**{mentor_type} 유형 설명**")
        st.write(TYPE_DESCRIPTIONS[mentor_type])

    available_time = st.selectbox(
        "주로 가능한 시간",
        [
            "평일",
            "주말",
            "저녁",
            "상관없음",
        ]
    )

    message = st.text_input(
        "한 줄 메시지",
        placeholder="예: 편하게 질문해도 괜찮아요!"
    )

    intro = st.text_area(
        "멘토 소개",
        placeholder="후배들에게 어떤 도움을 줄 수 있는지 간단히 적어주세요.",
        height=140
    )

    submitted = st.form_submit_button("멘토 등록하기", type="primary")


# -----------------------------
# 제출 처리
# -----------------------------
if submitted:
    if not name.strip():
        st.warning("이름을 입력해주세요.")
        st.stop()

    if not dept.strip():
        st.warning("학과를 입력해주세요.")
        st.stop()

    if not grade.strip():
        st.warning("학년을 입력해주세요.")
        st.stop()

    if not help_fields:
        st.warning("도움 가능 분야를 최소 1개 이상 선택해주세요.")
        st.stop()

    if not message.strip():
        st.warning("한 줄 메시지를 입력해주세요.")
        st.stop()

    if not intro.strip():
        st.warning("멘토 소개를 입력해주세요.")
        st.stop()

    mentor_profile = {
    "user_id": user.get("id"),
    "email": display_email,
    "name": name.strip(),
    "dept": dept.strip(),
    "grade": grade.strip(),
    "field": " · ".join(help_fields),
    "type": mentor_type,
    "type_description": TYPE_DESCRIPTIONS[mentor_type],
    "available_time": available_time,
    "message": message.strip(),
    "intro": intro.strip(),
    "status": "active",
}

try:
    # Supabase mentor_profiles 테이블에 저장
    saved_profile = save_mentor_profile(
        user_id=mentor_profile["user_id"],
        name=mentor_profile["name"],
        email=mentor_profile["email"],
        dept=mentor_profile["dept"],
        grade=mentor_profile["grade"],
        field=mentor_profile["field"],
        mentor_type=mentor_profile["type"],
        available_time=mentor_profile["available_time"],
        message=mentor_profile["message"],
        intro=mentor_profile["intro"],
    )

    if not saved_profile:
        st.error("멘토 정보 저장에 실패했습니다.")
        st.stop()

    # 화면 표시용으로 type_description 추가
    saved_profile["type_description"] = TYPE_DESCRIPTIONS.get(
        saved_profile.get("type"),
        ""
    )

    # 현재 화면에서도 바로 보이도록 session_state에 저장
    st.session_state.mentor_profile = saved_profile

    st.success("멘토 등록이 완료되었습니다!")
    st.info("멘토 정보가 Supabase DB에 저장되었습니다.")

    mentor_profile = saved_profile

except Exception as e:
    st.error(f"멘토 등록 중 오류가 발생했습니다: {e}")
    st.stop()

    with st.container(border=True):
        st.subheader("등록된 멘토 카드 미리보기")
        st.markdown(f"### 👩‍🎓 {mentor_profile['name']}")
        st.write(f"**학과:** {mentor_profile['dept']}")
        st.write(f"**학년:** {mentor_profile['grade']}")
        st.write(f"**도움 가능 분야:** {mentor_profile['field']}")
        st.write(f"**추천 후배 유형:** {mentor_profile['type']}")
        st.caption(mentor_profile["type_description"])
        st.write(f"**가능 시간:** {mentor_profile['available_time']}")
        st.write(f"**한 줄 메시지:** {mentor_profile['message']}")
        st.write(mentor_profile["intro"])


st.divider()


if st.button("홈으로 돌아가기", use_container_width=True):
    st.switch_page("app.py")



render_footer()
