# =========================================
# 매칭 유형 정의
# =========================================

TYPE_NAMES = [
    "열정송이",
    "새싹송이",
    "탐구송이",
    "소통송이",
]

TYPE_DESCRIPTIONS = {
    "열정송이": "목표가 생기면 끝까지 도전하는 열정적인 유형입니다.",
    "새싹송이": "새로운 환경에 적응하며 차근차근 성장하는 유형입니다.",
    "탐구송이": "새로운 기술과 지식을 배우는 것을 좋아하는 유형입니다.",
    "소통송이": "사람들과 함께 배우고 성장하는 것을 좋아하는 유형입니다.",
}

TYPE_EMOJI = {
    "열정송이": "🔥",
    "새싹송이": "🌱",
    "탐구송이": "🔍",
    "소통송이": "💬",
}


# =========================================
# 질문별 가중치
# Q5는 유형 분류에 사용하지 않음
# =========================================

QUESTION_WEIGHTS = {
    "q1": 0.25,
    "q2": 0.20,
    "q3": 0.15,
    "q4": 0.40,
}


# =========================================
# 질문별 점수표
# =========================================

SCORING_TABLE = {

    # Q1
    "q1": {
        "전공·학업": {
            "열정송이": 1,
            "새싹송이": 2,
            "탐구송이": 3,
            "소통송이": 1,
        },

        "진로·취업": {
            "열정송이": 3,
            "새싹송이": 2,
            "탐구송이": 2,
            "소통송이": 1,
        },

        "대학생활·인간관계": {
            "열정송이": 1,
            "새싹송이": 3,
            "탐구송이": 1,
            "소통송이": 3,
        },

        "특별한 고민 없음 (친해지고 싶어요!)": {
            "열정송이": 1,
            "새싹송이": 2,
            "탐구송이": 0,
            "소통송이": 3,
        },
    },


    # Q2
    "q2": {
        "경험 많고 조언을 잘해주는 송이": {
            "열정송이": 3,
            "새싹송이": 2,
            "탐구송이": 1,
            "소통송이": 2,
        },

        "전공·진로를 잘 알려주는 송이": {
            "열정송이": 3,
            "새싹송이": 1,
            "탐구송이": 3,
            "소통송이": 1,
        },

        "편하게 이야기할 수 있는 송이": {
            "열정송이": 1,
            "새싹송이": 2,
            "탐구송이": 0,
            "소통송이": 3,
        },

        "나와 공통점이 많은 송이": {
            "열정송이": 1,
            "새싹송이": 2,
            "탐구송이": 1,
            "소통송이": 3,
        },

        "새로운 경험을 공유할 수 있는 송이": {
            "열정송이": 3,
            "새싹송이": 2,
            "탐구송이": 3,
            "소통송이": 2,
        },
    },


    # Q3
    "q3": {
        "먼저 다가가는 편이에요": {
            "열정송이": 3,
            "새싹송이": 1,
            "탐구송이": 1,
            "소통송이": 3,
        },

        "처음엔 조심스럽지만 친해지면 편한 편이에요": {
            "열정송이": 1,
            "새싹송이": 3,
            "탐구송이": 1,
            "소통송이": 2,
        },

        "상대방 이야기를 잘 들어주는 편이에요": {
            "열정송이": 1,
            "새싹송이": 2,
            "탐구송이": 1,
            "소통송이": 3,
        },
    },


    # Q4
    "q4": {
        "성장": {
            "열정송이": 2,
            "새싹송이": 3,
            "탐구송이": 3,
            "소통송이": 2,
        },

        "도전": {
            "열정송이": 3,
            "새싹송이": 1,
            "탐구송이": 2,
            "소통송이": 1,
        },

        "좋은 인간관계": {
            "열정송이": 1,
            "새싹송이": 2,
            "탐구송이": 0,
            "소통송이": 3,
        },

        "삶의 균형 (학업, 일상, 취미 등의 균형)": {
            "열정송이": 2,
            "새싹송이": 3,
            "탐구송이": 1,
            "소통송이": 2,
        },
    },
}


# =========================================
# Q5 멘토링 가능 시간
# =========================================

TIME_OPTIONS = [
    "평일 오전",
    "평일 오후",
    "주말",
    "모두 가능해요",
]


# =========================================
# 유형 점수 계산
# =========================================

def calculate_type_scores(answers):

    scores = {
        type_name: 0.0
        for type_name in TYPE_NAMES
    }

    detail_scores = {}

    for question_key, weight in QUESTION_WEIGHTS.items():

        answer = answers.get(question_key)

        if answer is None:
            continue

        option_scores = SCORING_TABLE[question_key].get(answer)

        if option_scores is None:
            continue

        detail_scores[question_key] = {}

        for type_name in TYPE_NAMES:

            raw_score = option_scores[type_name]

            normalized_score = raw_score / 3

            weighted_score = (
                normalized_score
                * weight
                * 100
            )

            scores[type_name] += weighted_score

            detail_scores[question_key][type_name] = {
                "raw": raw_score,
                "weighted": weighted_score,
            }

    scores = {
        type_name: round(score, 2)
        for type_name, score in scores.items()
    }

    return scores, detail_scores


# =========================================
# 최종 유형 결정
# =========================================

def determine_type(scores):

    max_score = max(scores.values())

    candidates = [
        type_name
        for type_name, score in scores.items()
        if score == max_score
    ]

    return candidates[0]


# =========================================
# 최종 결과 생성
# =========================================

def get_matching_result(answers):

    scores, detail_scores = calculate_type_scores(
        answers
    )

    result_type = determine_type(scores)

    return {
        "type": result_type,
        "title": f"{result_type} 유형이에요!",
        "desc": TYPE_DESCRIPTIONS[result_type],
        "emoji": TYPE_EMOJI[result_type],
        "scores": scores,
        "detail_scores": detail_scores,
        "available_time": answers.get("q5"),
    }
