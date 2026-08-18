from utils.supabase_client import get_client


def upsert_profile(user_id: str, email: str, name: str, dept: str, grade: str):
    """
    profiles 테이블에 회원 기본 정보를 저장하거나 수정한다.
    """
    sb = get_client()

    data = {
        "id": user_id,
        "email": email,
        "name": name,
        "dept": dept,
        "grade": grade,
    }

    res = (
        sb.table("profiles")
        .upsert(data, on_conflict="id")
        .execute()
    )

    if res.data:
        return res.data[0]

    return data


def get_profile(user_id: str):
    """
    user_id 기준으로 profiles 테이블에서 내 정보를 가져온다.
    """
    sb = get_client()

    res = (
        sb.table("profiles")
        .select("*")
        .eq("id", user_id)
        .limit(1)
        .execute()
    )

    if res.data and len(res.data) > 0:
        return res.data[0]

    return None
