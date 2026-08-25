from utils.supabase_client import get_client


def save_matching_result(
    mentee_id: str,
    result: dict,
    answers: dict,
):
    """
    매칭 테스트 결과를 matching_results 테이블에 저장한다.
    """

    sb = get_client()

    data = {
        "mentee_id": mentee_id,
        "result_type": result.get("type"),
        "title": result.get("title"),
        "description": result.get("desc"),
        "answers": answers,
        "scores": result.get("scores", {}),
        "interest": answers.get("q2", ""),
        "purpose": answers.get("q1", ""),
        "preferred_time": answers.get("q5", ""),
    }

    res = (
        sb.table("matching_results")
        .insert(data)
        .execute()
    )

    if res.data and len(res.data) > 0:
        return res.data[0]

    return data


def get_latest_matching_result(mentee_id: str):
    """
    현재 로그인한 사용자의 가장 최근 매칭 결과를 가져온다.
    """

    sb = get_client()

    res = (
        sb.table("matching_results")
        .select("*")
        .eq("mentee_id", mentee_id)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )

    if res.data and len(res.data) > 0:
        return res.data[0]

    return None
