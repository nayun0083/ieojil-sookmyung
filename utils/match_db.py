from utils.supabase_client import get_client


def create_match_request(
    mentor_id: str,
    mentee_id: str,
    mentor_profile_id: str,
    result_type: str,
    topic: str,
    preferred_time: str,
    question: str,
):
    """멘티가 멘토에게 매칭 신청"""

    sb = get_client()

    res = (
        sb.table("matches")
        .insert({
            "mentor_id": mentor_id,
            "mentee_id": mentee_id,
            "mentor_profile_id": mentor_profile_id,
            "result_type": result_type,
            "topic": topic,
            "preferred_time": preferred_time,
            "question": question,
            "status": "pending",
        })
        .execute()
    )

    return res.data[0]

# =========================================================
# 알림 기능
# =========================================================

def get_sent_matches(user_id: str):
    """
    내가 멘티로서 보낸 매칭 신청 조회
    """
    sb = get_client()

    response = (
        sb.table("matches")
        .select("*")
        .eq("mentee_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )

    return response.data or []


def get_received_matches(user_id: str):
    """
    내가 멘토로서 받은 매칭 신청 조회
    """
    sb = get_client()

    response = (
        sb.table("matches")
        .select("*")
        .eq("mentor_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )

    return response.data or []


def update_match_status(match_id: str, status: str):
    """
    매칭 신청 상태 변경

    pending  = 수락 대기
    accepted = 수락 완료
    rejected = 거절
    """

    if status not in ["pending", "accepted", "rejected"]:
        raise ValueError("잘못된 상태값입니다.")

    sb = get_client()

    response = (
        sb.table("matches")
        .update({
            "status": status
        })
        .eq("id", match_id)
        .execute()
    )

    return response.data or []
