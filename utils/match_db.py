from utils.supabase_client import get_client


def create_match_request(
    mentor_id: str,
    mentee_id: str,
    mentor_profile_id: str,
    topic: str,
    preferred_field: str,
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
            "topic": topic,
            "preferred_field": preferred_field,
            "preferred_time": preferred_time,
            "question": question,
            "status": "pending",
        })
        .execute()
    )

    return res.data[0]
