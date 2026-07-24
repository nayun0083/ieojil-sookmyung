from utils.supabase_client import get_client


def create_match_request(mentor_id: str, mentee_id: str, result_type: str):
    """멘티가 멘토에게 매칭 신청"""
    sb = get_client()

    res = sb.table("matches").insert({
        "mentor_id": mentor_id,
        "mentee_id": mentee_id,
        "result_type": result_type,
        "status": "pending",
    }).execute()

    return res.data[0]


def get_pending_requests_for_mentor(mentor_id: str):
    """멘토가 받은 매칭 신청 목록"""
    sb = get_client()

    res = (
        sb.table("matches")
        .select("id, result_type, status, created_at, mentee:profiles!matches_mentee_id_fkey(name, dept, grade)")
        .eq("mentor_id", mentor_id)
        .eq("status", "pending")
        .order("created_at", desc=True)
        .execute()
    )

    return res.data or []


def accept_match(match_id: str):
    """멘토가 매칭 신청 수락"""
    sb = get_client()

    match_res = (
        sb.table("matches")
        .select("id, mentor_id, mentee_id")
        .eq("id", match_id)
        .single()
        .execute()
    )

    match = match_res.data

    if not match:
        return None, "매칭 정보를 찾을 수 없습니다."

    sb.table("matches").update({
        "status": "accepted"
    }).eq("id", match_id).execute()

    conv_res = sb.table("conversations").insert({
        "match_id": match["id"],
        "mentor_id": match["mentor_id"],
        "mentee_id": match["mentee_id"],
    }).execute()

    return conv_res.data[0], None