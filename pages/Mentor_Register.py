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


# -----------------------------
# 후배 유형 설명
# -----------------------------
TYPE_DESCRIPTIONS = {
    "새싹송이": "학교생활 적응, 수강신청, 전공 입문처럼 처음 시작하는 후배에게 잘 맞아요.",
    "탐구송이": "전공 공부, 개발, AI, 데이터 분석처럼 깊이 있게 배우고 싶은 후배에게 잘 맞아요.",
    "열정송이": "진로, 프로젝트, 대외활동처럼 목표를 가지고 도전하려는 후배에게 잘 맞아요.",
    "소통송이": "편안한 대화, 고민 상담, 학교생활 조언처럼 공감과 소통이 필요한 후배에게 잘 맞아요.",
}

HELP_FIELD_OPTIONS = [
    "학교생활",
    "수강신청",
    "전공 공부",
    "진로 고민",
    "대외활동",
    "프로젝트",
    "개발 공부",
    "고민 상담",
]

TIME_OPTIONS = [
    "평일",
    "주말",
    "저녁",
    "상관없음",
]
GRADE_OPTIONS = [1, 2, 3, 4]


def parse_grade(value):
    """
    기존 값이 1, '1', '1학년' 어떤 형태여도 숫자로 변환
    """
    value = str(value).replace("학년", "").strip()

    if value.isdigit():
        grade_num = int(value)
        if grade_num in GRADE_OPTIONS:
            return grade_num

    return 1

# -----------------------------
# 로그인 사용자 정보
# -----------------------------
user = get_current_user()
user = load_profile_user(user)

if not user or not user.get("id"):
    st.error("로그인 정보를 불러오지 못했습니다. 다시 로그인해주세요.")
    st.stop()

display_name = clean_name(user)
display_dept = user.get("dept") or user.get("department") or ""
display_grade = user.get("grade") or ""
display_email = user.get("email") or ""


# -----------------------------
# 세션 초기화
# -----------------------------
st.session_state.setdefault("mentor_profile", None)


# -----------------------------
# DB에 저장된 기존 멘토 정보 불러오기
# -----------------------------
existing_mentor_profile = None

try:
    existing_mentor_profile = get_mentor_profile_by_user(user["id"])
except Exception as e:
    st.warning(f"기존 멘토 정보를 불러오지 못했습니다: {e}")

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
# 현재 멘토 정보 가져오기
# -----------------------------
current_profile = st.session_state.get("mentor_profile")


# -----------------------------
# 기존 값 기본 세팅
# -----------------------------
default_name = current_profile.get("name", display_name) if current_profile else display_name
default_dept = current_profile.get("dept", display_dept) if current_profile else display_dept
default_grade = parse_grade(
    current_profile.get("grade", display_grade) if current_profile else display_grade
)
default_message = current_profile.get("message", "") if current_profile else ""
default_intro = current_profile.get("intro", "") if current_profile else ""

default_field_text = current_profile.get("field", "") if current_profile else ""
default_help_fields = [
    field.strip()
    for field in default_field_text.split("·")
    if field.strip() in HELP_FIELD_OPTIONS
]

mentor_type_options = ["선택해주세요"] + list(TYPE_DESCRIPTIONS.keys())

default_type = current_profile.get("type", "선택해주세요") if current_profile else "선택해주세요"
if default_type not in mentor_type_options:
    default_type = "선택해주세요"

default_time = current_profile.get("available_time", "평일") if current_profile else "평일"
if default_time not in TIME_OPTIONS:
    default_time = "평일"


# -----------------------------
# 멘토 등록 / 수정 입력 영역
# -----------------------------
st.subheader("멘토 정보 입력")
st.markdown("#### 기본 정보")
st.caption("회원가입 때 입력한 정보가 자동으로 들어옵니다. 잘못 보이면 이 화면에서 수정할 수 있어요.")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input(
        "이름",
        value=default_name,
        placeholder="예: 김숙명"
    )

    dept = st.text_input(
        "학과",
        value=default_dept,
        placeholder="예: 데이터사이언스학과"
    )

with col2:
    grade = st.selectbox(
        "학년",
        GRADE_OPTIONS,
        index=GRADE_OPTIONS.index(default_grade),
        format_func=lambda x: f"{x}학년"
    )

    email = st.text_input(
        "학교 이메일",
        value=display_email,
        disabled=True
    )

st.markdown("#### 멘토 활동 정보")

help_fields = st.multiselect(
    "도움 가능 분야",
    HELP_FIELD_OPTIONS,
    default=default_help_fields,
    help="후배에게 도움을 줄 수 있는 분야를 선택해주세요."
)

mentor_type = st.selectbox(
    "어떤 유형의 후배와 잘 맞나요?",
    mentor_type_options,
    index=mentor_type_options.index(default_type)
)

# 유형 설명: form 밖에 있으므로 선택할 때마다 바로 바뀜
if mentor_type != "선택해주세요":
    with st.container(border=True):
        st.markdown(f"**{mentor_type} 유형 설명**")
        st.write(TYPE_DESCRIPTIONS[mentor_type])

available_time = st.selectbox(
    "주로 가능한 시간",
    TIME_OPTIONS,
    index=TIME_OPTIONS.index(default_time)
)

message = st.text_input(
    "한 줄 메시지",
    value=default_message,
    placeholder="예: 편하게 질문해도 괜찮아요!"
)

intro = st.text_area(
    "멘토 소개",
    value=default_intro,
    placeholder="후배들에게 어떤 도움을 줄 수 있는지 간단히 적어주세요.",
    height=140
)


# -----------------------------
# 등록 / 수정 버튼
# -----------------------------
is_edit_mode = current_profile is not None

if is_edit_mode:
    submitted = st.button(
        "멘토 정보 수정하기",
        type="primary",
        use_container_width=True
    )
else:
    submitted = st.button(
        "멘토 등록하기",
        type="primary",
        use_container_width=True
    )


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

    if grade not in GRADE_OPTIONS:
        st.warning("학년을 선택해주세요.")
        st.stop()

    if not help_fields:
        st.warning("도움 가능 분야를 최소 1개 이상 선택해주세요.")
        st.stop()

    if mentor_type == "선택해주세요":
        st.warning("추천 후배 유형을 선택해주세요.")
        st.stop()

    if not message.strip():
        st.warning("한 줄 메시지를 입력해주세요.")
        st.stop()

    if not intro.strip():
        st.warning("멘토 소개를 입력해주세요.")
        st.stop()

    try:
        saved_profile = save_mentor_profile(
            user_id=user["id"],
            name=name.strip(),
            email=display_email,
            dept=dept.strip(),
            grade=grade,
            field=" · ".join(help_fields),
            mentor_type=mentor_type,
            available_time=available_time,
            message=message.strip(),
            intro=intro.strip(),
        )

        if not saved_profile:
            st.error("멘토 정보 저장에 실패했습니다.")
            st.stop()

        saved_profile["type_description"] = TYPE_DESCRIPTIONS.get(
            saved_profile.get("type"),
            ""
        )

        st.session_state.mentor_profile = saved_profile

        if is_edit_mode:
            st.success("멘토 정보가 수정되었습니다!")
        else:
            st.success("멘토 등록이 완료되었습니다!")

        st.info("멘토 정보가 Supabase DB에 저장되었습니다.")
        st.rerun()

    except Exception as e:
        st.error(f"멘토 등록/수정 중 오류가 발생했습니다: {e}")
        st.stop()

# -----------------------------
# 등록된 멘토 카드 미리보기
# -----------------------------
current_mentor_profile = st.session_state.get("mentor_profile")

if current_mentor_profile:
    with st.container(border=True):
        st.subheader("등록된 멘토 카드 미리보기")
        st.markdown(f"### 👩‍🎓 {current_mentor_profile.get('name', '-')}")
        st.write(f"**학과:** {current_mentor_profile.get('dept', '-')}")
        st.write(f"**학년:** {current_mentor_profile.get('grade', '-')}")
        st.write(f"**도움 가능 분야:** {current_mentor_profile.get('field', '-')}")
        st.write(f"**추천 후배 유형:** {current_mentor_profile.get('type', '-')}")
        st.caption(current_mentor_profile.get("type_description", ""))
        st.write(f"**가능 시간:** {current_mentor_profile.get('available_time', '-')}")
        st.write(f"**한 줄 메시지:** {current_mentor_profile.get('message', '-')}")
        st.write(current_mentor_profile.get("intro", ""))


st.divider()

if st.button("홈으로 돌아가기", use_container_width=True):
    st.switch_page("app.py")

render_footer()
