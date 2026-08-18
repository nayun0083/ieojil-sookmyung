from utils.supabase_client import get_client

"""매칭 로직: 답변 딕셔너리 → 유형/설명/추천멘토 반환"""

TYPE_INFO = {
    "열정송이": {
        "title": "당신은 열정송이입니다!",
        "desc": "목표가 생기면 끝까지 도전하는 열정적인 유형입니다. "
                "진로, 프로젝트, 대외활동처럼 성장 경험을 나눠줄 멘토와 잘 맞아요.",
        "mentor": {"name": "김송이 선배", "dept": "컴퓨터과학과", "sid": "20학번",
                   "field": "진로 · 프로젝트 · 대외활동"},
    },
    "새싹송이": {
        "title": "당신은 새싹송이입니다!",
        "desc": "새로운 환경에서 차근차근 성장하고 싶은 유형입니다. "
                "학교생활과 전공 적응을 친절하게 도와줄 멘토와 잘 맞아요.",
        "mentor": {"name": "박새롬 선배", "dept": "소프트웨어학부", "sid": "22학번",
                   "field": "학교생활 · 수강신청 · 전공 적응"},
    },
    "탐구송이": {
        "title": "당신은 탐구송이입니다!",
        "desc": "궁금한 것을 깊이 있게 배우고 싶어 하는 유형입니다. "
                "전공 공부, 개발, AI 등 관심 분야를 구체적으로 알려줄 멘토와 잘 맞아요.",
        "mentor": {"name": "이탐구 선배", "dept": "데이터사이언스학과", "sid": "21학번",
                   "field": "AI · 데이터분석 · 전공 공부"},
    },
    "소통송이": {
        "title": "당신은 소통송이입니다!",
        "desc": "편안한 대화와 공감을 통해 성장하는 유형입니다. "
                "친구처럼 고민을 나누고 경험을 공유할 수 있는 멘토와 잘 맞아요.",
        "mentor": {"name": "최다정 선배", "dept": "미디어학부", "sid": "21학번",
                   "field": "학교생활 · 고민상담 · 커뮤니케이션"},
    },
}

# 동점 시 Q4 성향 → 유형 매핑
TIE_BREAK = {"도전형": "열정송이", "계획형": "탐구송이",
             "신중형": "새싹송이", "사교형": "소통송이"}


def calculate_scores(answers: dict) -> dict:
    scores = {"열정송이": 0, "새싹송이": 0, "탐구송이": 0, "소통송이": 0}

    # Q1 도움 분야
    q1 = answers.get("q1")
    if q1 == "학교생활":
        scores["새싹송이"] += 2
    elif q1 == "전공":
        scores["탐구송이"] += 2
    elif q1 == "취업":
        scores["열정송이"] += 2
    elif q1 == "대외활동":
        scores["열정송이"] += 1
        scores["소통송이"] += 1

    # Q1-1 자유응답 키워드
    text = str(answers.get("q1_1", ""))
    kw = {
        "소통송이": ["친구", "관계", "소통", "적응"],
        "탐구송이": ["수업", "학점", "전공", "공부"],
        "열정송이": ["진로", "취업", "스펙", "대외활동", "프로젝트"],
        "새싹송이": ["학교생활", "수강신청", "동아리", "생활"],
    }
    matched = False
    for t, words in kw.items():
        if any(w in text for w in words):
            scores[t] += 2
            matched = True
    if not matched:
        scores["새싹송이"] += 1

    # Q2 관심 분야
    q2 = answers.get("q2")
    if q2 == "AI":
        scores["탐구송이"] += 2
    elif q2 == "웹개발":
        scores["탐구송이"] += 2
    elif q2 == "앱개발":
        scores["탐구송이"] += 1
        scores["열정송이"] += 1
    elif q2 == "디자인":
        scores["소통송이"] += 1
        scores["열정송이"] += 1

    # Q3 원하는 선배
    q3 = answers.get("q3")
    m3 = {"친절한": "새싹송이", "친구 같은": "소통송이",
          "경험 많은": "열정송이", "꼼꼼한": "탐구송이"}
    if q3 in m3:
        scores[m3[q3]] += 2

    # Q4 성향
    q4 = answers.get("q4")
    m4 = {"도전형": "열정송이", "계획형": "탐구송이",
          "신중형": "새싹송이", "사교형": "소통송이"}
    if q4 in m4:
        scores[m4[q4]] += 2

    # Q5 가능 시간
    q5 = answers.get("q5")
    m5 = {"평일": "탐구송이", "주말": "열정송이",
          "저녁": "소통송이", "상관없음": "새싹송이"}
    if q5 in m5:
        scores[m5[q5]] += 1

    return scores


def get_matching_result(answers: dict) -> dict:

    scores = calculate_scores(answers)

    max_score = max(scores.values())

    top = [
        t for t, s in scores.items()
        if s == max_score
    ]

    if len(top) == 1:

        result_type = top[0]

    else:

        # 동점 → Q4 성향 우선
        result_type = TIE_BREAK.get(
            answers.get("q4"),
            top[0]
        )

        if result_type not in top:
            result_type = top[0]


    info = TYPE_INFO[result_type]


    # --------------------------------
    # 실제 멘토 프로필 조회
    # --------------------------------

    sb = get_client()

    res = (
        sb.table("mentor_profiles")
        .select("*")
        .eq("type", result_type)
        .limit(1)
        .execute()
    )


    # DB에서 멘토를 찾은 경우
    if res.data:

        db_mentor = res.data[0]

        mentor = {
            "id": db_mentor["id"],
            "user_id": db_mentor["user_id"],
            "name": db_mentor["name"],
            "dept": db_mentor["dept"],
            "sid": db_mentor["grade"],
            "field": db_mentor["field"],
            "email": db_mentor.get("email", ""),
            "available_time": db_mentor.get(
                "available_time",
                ""
            ),
            "intro": db_mentor.get(
                "intro",
                ""
            ),
        }

    # DB에 멘토가 없는 경우
    else:

        mentor = info["mentor"]


    return {
        "type": result_type,
        "title": info["title"],
        "desc": info["desc"],
        "mentor": mentor,
        "scores": scores,
    }
