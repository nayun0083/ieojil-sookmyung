"""인증 로직 - 숙명여대 이메일 전용 회원가입/로그인/가드"""

import streamlit as st
from utils.supabase_client import get_client

ALLOWED_DOMAIN = "@sookmyung.ac.kr"


def is_sookmyung_email(email: str) -> bool:
    """숙명여대 학교 이메일인지 검증"""
    return email.strip().lower().endswith(ALLOWED_DOMAIN)


def sign_up(name, email, password, dept, grade):
    """회원가입: Supabase Auth 계정 생성 + profiles 테이블 저장"""

    email = email.strip().lower()

    if not is_sookmyung_email(email):
        return None, "숙명여대 학교 이메일 계정만 사용할 수 있습니다."

    sb = get_client()

    try:
        # 1. Supabase Auth 계정 생성
        res = sb.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "name": name,
                    "dept": dept,
                    "grade": grade,
                    "role": "사용자"
                }
            },
        })

        user = res.user

        if user is None:
            return None, "회원가입에 실패했습니다. 다시 시도해주세요."

        # 2. profiles 테이블에 사용자 정보 저장
        sb.table("profiles").upsert({
            "id": user.id,
            "name": name,
            "email": email,
            "dept": dept,
            "grade": grade,
            "role": "사용자",
        }).execute()

        return user, None

    except Exception as e:
        msg = str(e)

        if "already registered" in msg or "already been registered" in msg:
            return None, "이미 가입된 이메일입니다."

        return None, f"회원가입 오류: {msg}"


def sign_in(email, password):
    """로그인: 도메인 검증 후 인증, 프로필 조회"""

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

        if res.user is None:
            return None, "이메일 또는 비밀번호가 올바르지 않습니다."

        # 2. profiles 테이블에서 사용자 정보 조회
        profile = (
            sb.table("profiles")
            .select("*")
            .eq("id", res.user.id)
            .single()
            .execute()
        )

        user_info = profile.data or {
            "id": res.user.id,
            "email": email,
        }

        st.session_state.current_user = user_info

        return user_info, None

    except Exception as e:
        msg = str(e)

        if "Invalid login credentials" in msg:
            return None, "이메일 또는 비밀번호가 올바르지 않습니다."

        if "Email not confirmed" in msg:
            return None, "이메일 인증이 필요합니다. 메일함을 확인해주세요."

        return None, f"로그인 오류: {msg}"


def sign_out():
    """로그아웃"""

    try:
        get_client().auth.sign_out()
    except Exception:
        pass

    st.session_state.current_user = None


def get_current_user():
    """현재 로그인한 사용자 정보 반환"""
    return st.session_state.get("current_user")


def is_logged_in() -> bool:
    """로그인 여부 확인"""
    return st.session_state.get("current_user") is not None


def require_login():
    """보호된 페이지 상단에서 호출. 미로그인 시 로그인 페이지 안내"""

    if not is_logged_in():
        st.warning("🔒 로그인이 필요한 기능입니다.")
        st.info("로그인 페이지로 이동해주세요.")

        if st.button("로그인 하러 가기", type="primary"):
            st.switch_page("pages/Login.py")

        st.stop()