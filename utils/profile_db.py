from utils.supabase_client import get_client


def upsert_profile(user_id: str, email: str, name: str, dept: str, grade: str, sb=None):
    """
    profiles 테이블에 회원 기본 정보를 저장하거나 수정한다.
    sb가 전달되면 그 로그인된 client를 사용한다.
    """
    if sb is None:
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

    return res.data[0] if res.data else data


def get_profile(user_id: str, sb=None):
    """
    user_id 기준으로 profiles 테이블에서 내 정보를 가져온다.
    sb가 전달되면 그 로그인된 client를 사용한다.
    """
    if sb is None:
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
