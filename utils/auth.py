"""인증 로직 - 숙명여대 이메일 전용 회원가입/로그인/가드"""

import streamlit as st

from utils.supabase_client import get_client
from utils.profile_db import upsert_profile, get_profile


ALLOWED_DOMAIN = "@sookmyung.ac.kr"


def is_sookmyung_email(email: str) -> bool:
    return email.strip().lower().endswith(ALLOWED_DOMAIN)


def sign_up(name, email, password, dept, grade, role=None):
    """
    회원가입
    1. Supabase Auth에 계정 생성
    2. profiles 테이블에 회원 기본 정보 저장

    role은 예전 코드와 호환하려고 받기만 하고 사용하지 않음
    """
    email = email.strip().lower()

    if not is_sookmyung_email(email):
        return None, "숙명여대 학교 이메일 계정만 사용할 수 있습니다."

    sb = get_client()

    try:
        # 1. Supabase Auth 회원가입
        res = sb.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "name": name,
                    "dept": dept,
                    "grade": grade,
                }
            },
        })

        user = res.user

        if user is None:
            return None, "회원가입에 실패했습니다. 다시 시도해주세요."

        # 2. profiles 테이블에 회원정보 저장
        profile = upsert_profile(
            user_id=user.id,
            email=email,
            name=name,
            dept=dept,
            grade=grade,
        )

        return profile, None

    except Exception as e:
        msg = str(e)

        if "already registered" in msg or "already been registered" in msg:
            return None, "이미 가입된 이메일입니다."

        return None, f"회원가입 오류: {msg}"


def sign_in(email, password):
    """
    로그인
    1. Supabase Auth 로그인
    2. profiles 테이블에서 내 정보 조회
    3. session_state.current_user에 저장
    """
    email = email.strip().lower()

    if not is_sookmyung_email(email):
        return None, "숙명여대 학교 이메일 계정만 사용할 수 있습니다."

    sb = get_client()

    try:
        # 1. Supabase Auth 로그인
        res = sb.auth.sign_in_with_password({
            "email": email,
            "password": password,
        })

        user = res.user

        if user is None:
            return None, "이메일 또는 비밀번호가 올바르지 않습니다."

        # 2. profiles에서 회원정보 가져오기
        profile = get_profile(user.id)

        # 혹시 profiles에 정보가 없으면 metadata로 다시 생성
        if profile is None:
            metadata = user.user_metadata or {}

            profile = upsert_profile(
                user_id=user.id,
                email=email,
                name=metadata.get("name", "사용자"),
                dept=metadata.get("dept", "-"),
                grade=metadata.get("grade", "-"),
            )

        # 3. 로그인한 사용자 정보를 session_state에 저장
        st.session_state.current_user = profile

        return profile, None

    except Exception as e:
        msg = str(e)

        if "Invalid login credentials" in msg:
            return None, "이메일 또는 비밀번호가 올바르지 않습니다."

        if "Email not confirmed" in msg:
            return None, "이메일 인증이 필요합니다. 메일함을 확인해주세요."

        return None, f"로그인 오류: {msg}"


def sign_out():
    try:
        get_client().auth.sign_out()
    except Exception:
        pass

    st.session_state.current_user = None


def get_current_user():
    return st.session_state.get("current_user")


def is_logged_in() -> bool:
    return st.session_state.get("current_user") is not None


def require_login():
    if not is_logged_in():
        st.warning("🔒 로그인이 필요한 기능입니다.")
        st.info("로그인 페이지로 이동해주세요.")

        if st.button("로그인 하러 가기", type="primary"):
            st.switch_page("pages/Login.py")

        st.stop()
