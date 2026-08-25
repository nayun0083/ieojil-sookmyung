from utils.supabase_client import get_client

def create_match_request(
    mentor_id: str,
    mentee_id: str,
    mentor_profile_id: str,
    result_type: str,
    topic: str,
    preferred_time: str,
    question: str,
    preferred_field: str = "",
    mentor_name: str = "",
    mentee_name: str = "",
    mentee_dept: str = "",
    mentee_grade: str = "",
    main_question: str = "",
    mentoring_method: str = "",
    schedule_1: str = "",
    schedule_2: str = "",
    schedule_3: str = "",
):
    """
    멘티가 멘토에게 멘토링 신청서를 제출한다.
    """

    sb = get_client()

    data = {
        "mentor_id": mentor_id,
        "mentee_id": mentee_id,
        "mentor_profile_id": mentor_profile_id,
        "result_type": result_type,
        "topic": topic,
        "preferred_time": preferred_time,
        "question": question,
        "preferred_field": preferred_field,
        "mentor_name": mentor_name,
        "mentee_name": mentee_name,
        "mentee_dept": mentee_dept,
        "mentee_grade": str(mentee_grade),
        "main_question": main_question,
        "mentoring_method": mentoring_method,
        "schedule_1": schedule_1,
        "schedule_2": schedule_2,
        "schedule_3": schedule_3,
        "status": "pending",
    }

    res = (
        sb.table("matches")
        .insert(data)
        .execute()
    )

    if res.data and len(res.data) > 0:
        return res.data[0]

    return data



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


def update_match_status(
    match_id: str,
    status: str,
    accepted_schedule: str = "",
    openchat_password: str = "",
    openchat_link: str = "",
):
    """
    매칭 신청 상태 변경

    pending  = 수락 대기
    accepted = 수락 완료
    rejected = 거절
    """

    if status not in ["pending", "accepted", "rejected"]:
        raise ValueError("잘못된 상태값입니다.")

    sb = get_client()

    data = {
        "status": status
    }

    if accepted_schedule:
        data["accepted_schedule"] = accepted_schedule

    if openchat_password:
        data["openchat_password"] = openchat_password

    if openchat_link:
        data["openchat_link"] = openchat_link

    response = (
        sb.table("matches")
        .update(data)
        .eq("id", match_id)
        .execute()
    )

    return response.data or []

def save_mentor_reply(match_id: str, mentor_reply: str):
    """
    멘토가 신청서에 대한 답변을 저장한다.
    알림 페이지에서 나중에 사용할 수 있는 함수.
    """
    sb = get_client()

    response = (
        sb.table("matches")
        .update({
            "mentor_reply": mentor_reply
        })
        .eq("id", match_id)
        .execute()
    )

    return response.data or []
