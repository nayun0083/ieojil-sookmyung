import inspect
import streamlit as st

from components.header import render_header
from components.footer import render_footer
from utils.auth import (
    sign_in,
    sign_up,
    sign_out,
    get_current_user,
    is_logged_in,
)

st.set_page_config(
    page_title="로그인 · 이어질 숙명",
    page_icon="💙",
    layout="wide"
)

render_header(active="login")


def call_sign_up(name, email, password, dept, grade):
    """
    auth.py의 sign_up 함수가 role을 받는 버전이어도,
    role을 안 받는 버전이어도 둘 다 작동하도록 처리
    """
    params = inspect.signature(sign_up).parameters

    if "role" in params:
        return sign_up(name, email, password, dept, grade, "사용자")

    return sign_up(name, email, password, dept, grade)


st.title("로그인 / 회원가입")
st.caption("숙명여대 학교 이메일 계정으로 이용할 수 있어요.")

st.divider()


# -----------------------------
# 이미 로그인한 경우: 내 계정 화면
# -----------------------------
if is_logged_in():
    user = get_current_user()

    st.subheader("내 계정")

    with st.container(border=True):
        st.write(f"**이름:** {user.get('name', '-')}")
        st.write(f"**이메일:** {user.get('email', '-')}")
        st.write(f"**학과:** {user.get('dept', '-')}")
        st.write(f"**학년:** {user.get('grade', '-')}")

    st.write("")

    c1, c2 = st.columns(2)

    with c1:
        if st.button("멘토 등록하기", type="primary", use_container_width=True):
            st.switch_page("pages/Mentor_Register.py")

    with c2:
        if st.button("홈으로 돌아가기", use_container_width=True):
            st.switch_page("app.py")

    st.write("")

    if st.button("로그아웃", use_container_width=True):
        sign_out()
        st.success("로그아웃되었습니다.")
        st.rerun()

    render_footer()
    st.stop()


# -----------------------------
# 로그인 / 회원가입 탭
# -----------------------------
login_tab, signup_tab = st.tabs(["로그인", "회원가입"])


# -----------------------------
# 로그인
# -----------------------------
with login_tab:
    st.subheader("로그인")
    st.write("가입한 학교 이메일과 비밀번호로 로그인해주세요.")

    email = st.text_input(
        "학교 이메일",
        placeholder="example@sookmyung.ac.kr",
        key="login_email"
    )

    password = st.text_input(
        "비밀번호",
        type="password",
        key="login_password"
    )

    if st.button("로그인", type="primary", use_container_width=True):
        if not email.strip():
            st.warning("이메일을 입력해주세요.")
            st.stop()

        if not password.strip():
            st.warning("비밀번호를 입력해주세요.")
            st.stop()

        user, err = sign_in(email, password)

        if err:
            st.error(err)
        else:
            st.success("로그인되었습니다.")
            st.rerun()


# -----------------------------
# 회원가입
# -----------------------------
with signup_tab:
    st.subheader("회원가입")
    st.write("회원가입 후 이메일 인증이 필요한 경우, 메일함에서 인증을 완료해주세요.")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input(
            "이름",
            placeholder="예: 김숙명",
            key="signup_name"
        )

        dept = st.text_input(
            "학과",
            placeholder="예: 데이터사이언스학과",
            key="signup_dept"
        )

        grade = st.selectbox(
            "학년",
            ["1학년", "2학년", "3학년", "4학년", "졸업생"],
            key="signup_grade"
        )

    with col2:
        signup_email = st.text_input(
            "학교 이메일",
            placeholder="example@sookmyung.ac.kr",
            key="signup_email"
        )

        signup_password = st.text_input(
            "비밀번호",
            type="password",
            key="signup_password"
        )

        signup_password_check = st.text_input(
            "비밀번호 확인",
            type="password",
            key="signup_password_check"
        )

    if st.button("회원가입", type="primary", use_container_width=True):
        if not name.strip():
            st.warning("이름을 입력해주세요.")
            st.stop()

        if not dept.strip():
            st.warning("학과를 입력해주세요.")
            st.stop()

        if not signup_email.strip():
            st.warning("학교 이메일을 입력해주세요.")
            st.stop()

        if not signup_password.strip():
            st.warning("비밀번호를 입력해주세요.")
            st.stop()

        if signup_password != signup_password_check:
            st.warning("비밀번호가 일치하지 않습니다.")
            st.stop()

        if len(signup_password) < 6:
            st.warning("비밀번호는 6자 이상 입력해주세요.")
            st.stop()

        user, err = call_sign_up(
            name=name,
            email=signup_email,
            password=signup_password,
            dept=dept,
            grade=grade
        )

        if err:
            st.error(err)
        else:
            st.success("회원가입 요청이 완료되었습니다!")
            st.info("이메일 인증이 필요한 경우, 학교 이메일 메일함에서 인증을 완료한 뒤 로그인해주세요.")

render_footer()
