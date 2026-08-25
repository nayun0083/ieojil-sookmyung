from datetime import datetime, timezone

from utils.supabase_client import get_client


def save_mentor_profile(
    user_id: str,
    name: str,
    email: str,
    dept: str,
    grade,
    field: str,
    mentor_type: str,
    available_time: str,
    message: str,
    intro: str,
    openchat_link: str = "",
):
    """
    멘토 등록 정보 저장 함수

    이미 등록한 멘토 정보가 있으면 수정(update)하고,
    없으면 새로 등록(insert)한다.
    """

    sb = get_client()

    data = {
        "user_id": user_id,
        "name": name,
        "email": email,
        "dept": dept,
        "grade": grade,
        "field": field,
        "type": mentor_type,
        "available_time": available_time,
        "message": message,
        "intro": intro,
        "status": "active",
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "openchat_link": openchat_link,
    }

    # 기존 멘토 정보 확인
    existing = (
        sb.table("mentor_profiles")
        .select("*")
        .eq("user_id", user_id)
        .limit(1)
        .execute()
    )

    # 이미 있으면 update
    if existing.data and len(existing.data) > 0:
        existing_id = existing.data[0].get("id")

        res = (
            sb.table("mentor_profiles")
            .update(data)
            .eq("user_id", user_id)
            .execute()
        )

        # Supabase가 수정된 데이터를 돌려주면 그걸 사용
        if res.data and len(res.data) > 0:
            return res.data[0]

        # res.data가 비어 있으면 다시 조회해서 반환
        updated = (
            sb.table("mentor_profiles")
            .select("*")
            .eq("user_id", user_id)
            .limit(1)
            .execute()
        )

        if updated.data and len(updated.data) > 0:
            return updated.data[0]

        # 그래도 없으면 화면 표시용 fallback 반환
        data["id"] = existing_id
        return data

    # 없으면 insert
    res = (
        sb.table("mentor_profiles")
        .insert(data)
        .execute()
    )

    if res.data and len(res.data) > 0:
        return res.data[0]

    # insert 후에도 data가 비어 있으면 다시 조회
    created = (
        sb.table("mentor_profiles")
        .select("*")
        .eq("user_id", user_id)
        .limit(1)
        .execute()
    )

    if created.data and len(created.data) > 0:
        return created.data[0]

    return data


def get_mentor_profile_by_user(user_id: str):
    """
    현재 로그인한 사용자의 멘토 등록 정보를 가져온다.
    """

    sb = get_client()

    res = (
        sb.table("mentor_profiles")
        .select("*")
        .eq("user_id", user_id)
        .limit(1)
        .execute()
    )

    return res.data[0] if res.data else None


def get_active_mentor_profiles():
    """
    활성화된 전체 멘토 목록을 가져온다.
    매칭 결과 페이지에서 추천 멘토 목록으로 사용할 수 있다.
    """

    sb = get_client()

    res = (
        sb.table("mentor_profiles")
        .select("*")
        .eq("status", "active")
        .order("created_at", desc=True)
        .execute()
    )

    return res.data or []


def get_mentor_profile_by_id(mentor_profile_id: str):
    """
    mentor_profile_id 기준으로 특정 멘토 정보를 가져온다.
    매칭 신청 페이지나 멘토 프로필 상세보기에서 사용할 수 있다.
    """

    sb = get_client()

    res = (
        sb.table("mentor_profiles")
        .select("*")
        .eq("id", mentor_profile_id)
        .limit(1)
        .execute()
    )

    return res.data[0] if res.data else None

def get_mentors_by_type(result_type: str):
    """
    매칭 결과 유형에 맞는 멘토만 조회
    """
    sb = get_client()

    res = (
        sb.table("mentor_profiles")
        .select("*")
        .eq("status", "active")
        .eq("type", result_type)
        .order("created_at", desc=True)
        .execute()
    )

    return res.data or []

