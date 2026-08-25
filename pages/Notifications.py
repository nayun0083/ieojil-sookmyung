import streamlit as st

from components.header import render_header
from components.footer import render_footer
from utils.auth import require_login, get_current_user

from utils.match_db import (
    get_sent_matches,
    get_received_matches,
    update_match_status,
)

from utils.mentor_db import get_mentor_profile_by_id


# =========================================================
# 페이지 설정
# =========================================================

st.set_page_config(
    page_title="알림 · 이어질 숙명",
    layout="wide",
    page_icon="💙"
)


# =========================================================
# 기본 설정
# =========================================================

render_header(active="noti")
require_login()

user = get_current_user()

if not user:
    st.error("로그인 정보를 찾을 수 없습니다.")
    st.stop()

user_id = user.get("id") if isinstance(user, dict) else user.id


st.title("알림")
st.caption("매칭 신청 현황과 받은 요청을 확인할 수 있어요.")

st.divider()


# =========================================================
# 유틸 함수
# =========================================================

def clean_value(value, default="-"):
    """
    None, 빈 문자열, 'None' 문자열을 화면에 그대로 보여주지 않기 위한 함수
    """

    if value is None:
        return default

    value = str(value).strip()

    if value == "" or value.lower() == "none":
        return default

    return value


def get_status_text(status: str):
    """
    상태값을 화면용 문구로 변환
    """

    if status == "pending":
        return "수락 대기 중"

    if status == "accepted":
        return "수락 완료"

    if status == "rejected":
        return "거절됨"

    return clean_value(status)


def extract_application_value(question_text: str, label: str):
    """
    question에 저장된 신청서 텍스트에서 특정 항목만 꺼내기
    예: 핵심 질문 1:, 핵심 질문 2:, 현재 상황:
    """

    if not question_text:
        return "-"

    lines = str(question_text).split("\n")

    for line in lines:
        line = line.strip()

        if line.startswith(label):
            value = line.replace(label, "", 1).strip()
            return clean_value(value)

    return "-"


def get_mentor_display_name(match):
    """
    내 신청 현황에서 mentor_id UUID 대신 멘토 이름을 보여주기
    """

    mentor_name = clean_value(
        match.get("mentor_name"),
        default=""
    )

    if mentor_name:
        return mentor_name

    mentor_profile_id = match.get("mentor_profile_id")

    if mentor_profile_id:
        try:
            mentor_profile = get_mentor_profile_by_id(mentor_profile_id)

            if mentor_profile:
                return clean_value(
                    mentor_profile.get("name"),
                    default="멘토"
                )

        except Exception:
            pass

    return "멘토"

def get_mentor_openchat_link(match):
    """
    matches에 저장된 openchat_link가 있으면 사용하고,
    없으면 mentor_profile_id로 mentor_profiles에서 가져온다.
    """

    openchat_link = clean_value(
        match.get("openchat_link"),
        default=""
    )

    if openchat_link:
        return openchat_link

    mentor_profile_id = match.get("mentor_profile_id")

    if mentor_profile_id:
        try:
            mentor_profile = get_mentor_profile_by_id(mentor_profile_id)

            if mentor_profile:
                return clean_value(
                    mentor_profile.get("openchat_link"),
                    default=""
                )

        except Exception:
            pass

    return ""

def render_application_detail(match, mode="sent"):
    """
    멘토링 신청서 전체 내용을 가독성 좋게 보여주는 UI

    mode="sent"     내가 보낸 신청서 보기
    mode="received" 멘토가 받은 신청서 보기
    """

    question_text = match.get("question", "")

    mentor_name = get_mentor_display_name(match)

    mentee_name = clean_value(
        match.get("mentee_name"),
        default="멘티"
    )

    mentee_dept = clean_value(
        match.get("mentee_dept")
    )

    mentee_grade = clean_value(
        match.get("mentee_grade")
    )

    result_type = clean_value(
        match.get("result_type")
    )

    topic = clean_value(
        match.get("topic")
    )

    preferred_field = clean_value(
        match.get("preferred_field")
    )

    main_question = clean_value(
        match.get("main_question"),
        default=""
    )

    if not main_question:
        main_question = extract_application_value(
            question_text,
            "핵심 질문 1:"
        )

    question_2 = extract_application_value(
        question_text,
        "핵심 질문 2:"
    )

    background = extract_application_value(
        question_text,
        "현재 상황:"
    )

    mentoring_method = clean_value(
    match.get("mentoring_method")
    )

    if mentoring_method == "-":
        mentoring_method = extract_application_value(
            question_text,
            "희망 방식:"
        )
    
    
    schedule_1 = clean_value(
        match.get("schedule_1")
    )
    
    if schedule_1 == "-":
        schedule_1 = extract_application_value(
            question_text,
            "1순위:"
        )
    
    
    schedule_2 = clean_value(
        match.get("schedule_2")
    )
    
    if schedule_2 == "-":
        schedule_2 = extract_application_value(
            question_text,
            "2순위:"
        )
    
    
    schedule_3 = clean_value(
        match.get("schedule_3")
    )
    
    if schedule_3 == "-":
        schedule_3 = extract_application_value(
            question_text,
            "3순위:"
        )

    

    st.markdown("### 📄 멘토링 신청서")

    # -----------------------------------------
    # 멘토/멘티 정보
    # -----------------------------------------

    with st.container(border=True):

        if mode == "sent":
            st.markdown("#### 📌 멘토 정보")
            st.write(f"**이름:** {mentor_name}")
            st.write(f"**매칭 유형:** {result_type}")

        else:
            st.markdown("#### 📌 멘티 정보")
            st.write(f"**이름:** {mentee_name}")
            st.write(f"**전공 / 학년:** {mentee_dept} / {mentee_grade}")
            st.write(f"**매칭 유형:** {result_type}")


    # -----------------------------------------
    # 신청 분야
    # -----------------------------------------

    with st.container(border=True):
        st.markdown("#### 🧭 신청 분야")

        st.write(f"**신청 주제:** {topic}")
        st.write(f"**세부 진로/관심 분야:** {preferred_field}")


    # -----------------------------------------
    # 핵심 질문
    # -----------------------------------------

    with st.container(border=True):
        st.markdown("#### ❓ 핵심 질문")

        st.write("**질문 1**")

        if main_question and main_question != "-":
            st.markdown(f"> {main_question}")

        else:
            st.info("질문 1이 입력되지 않았습니다.")

        if question_2 and question_2 != "-":
            st.write("**질문 2**")
            st.markdown(f"> {question_2}")


    # -----------------------------------------
    # 현재 상황
    # -----------------------------------------

    if background and background != "-":
        with st.container(border=True):
            st.markdown("#### 📝 현재 상황")
            st.write(background)


    # -----------------------------------------
    # 멘토링 방식과 일정
    # -----------------------------------------

    with st.container(border=True):
        st.markdown("#### 🗓 멘토링 방식과 희망 일정")

        st.write(f"**희망 방식:** {mentoring_method}")
        st.write(f"**1순위:** {schedule_1}")
        st.write(f"**2순위:** {schedule_2}")
        st.write(f"**3순위:** {schedule_3}")


def render_sent_match_card(match):
    """
    내가 보낸 신청 카드
    """

    mentor_name = get_mentor_display_name(match)

    status = clean_value(
        match.get("status"),
        default="pending"
    )

    result_type = clean_value(
        match.get("result_type")
    )

    topic = clean_value(
        match.get("topic")
    )

    preferred_time = clean_value(
        match.get("preferred_time")
    )
    question_text = match.get("question", "")

    mentoring_method = clean_value(
        match.get("mentoring_method")
    )
    
    if mentoring_method == "-":
        mentoring_method = extract_application_value(
            question_text,
            "희망 방식:"
        )
    
    schedule_1 = clean_value(
        match.get("schedule_1")
    )
    
    if schedule_1 == "-":
        schedule_1 = extract_application_value(
            question_text,
            "1순위:"
        )
    

    preferred_field = clean_value(
        match.get("preferred_field")
    )

    main_question = clean_value(
        match.get("main_question")
    )
    
    if main_question == "-":
        main_question = extract_application_value(
            question_text,
            "핵심 질문 1:"
        )

    accepted_schedule = clean_value(
        match.get("accepted_schedule")
    )


    with st.container(border=True):

        st.markdown("### 👩‍🎓 매칭 신청")

        st.write(f"**멘토:** {mentor_name}")
        st.write(f"**희망 분야:** {preferred_field}")
        st.write(f"**주제:** {topic}")
        st.write(f"**핵심 질문:** {main_question}")
        st.write(f"**희망 방식:** {mentoring_method}")
        st.write(f"**1순위 일정:** {schedule_1}")
        st.write(f"**추천 유형:** {result_type}")


        # -----------------------------
        # 상태 표시
        # -----------------------------

        if status == "pending":

            st.warning("현재 상태: 수락 대기 중")

            st.write(
                "멘토가 신청을 확인하면 "
                "수락 여부가 표시됩니다."
            )


        elif status == "accepted":

            st.success("현재 상태: 매칭 수락 완료")
        
            openchat_link = clean_value(
                match.get("openchat_link"),
                default=""
            )
        
            openchat_password = clean_value(
                match.get("openchat_password"),
                default=""
            )
        
            if accepted_schedule and accepted_schedule != "-":
                st.write(f"**확정 일정:** {accepted_schedule}")
        
            st.write("멘토가 매칭 신청을 수락했습니다.")
        
            st.divider()
            st.markdown("#### 💬 오픈채팅방 입장 정보")
        
            if openchat_link:
                st.write(f"**오픈채팅방 링크:** {openchat_link}")
            else:
                st.info("아직 오픈채팅방 링크가 등록되지 않았습니다.")
        
            if openchat_password:
                st.write(f"**오픈채팅방 비밀번호:** `{openchat_password}`")
            else:
                st.info("아직 오픈채팅방 비밀번호가 전달되지 않았습니다.")


        elif status == "rejected":

            st.error("현재 상태: 매칭 거절")

            st.write(
                "멘토가 매칭 신청을 거절했습니다. "
                "다른 멘토에게 다시 신청할 수 있어요."
            )


        else:

            st.info(f"현재 상태: {status}")


        with st.expander("📄 내가 보낸 멘토링 신청서 보기"):
            render_application_detail(
                match,
                mode="sent"
            )


def render_received_match_card(match):
    """
    내가 받은 신청 카드
    """

    match_id = match.get("id")

    status = clean_value(
        match.get("status"),
        default="pending"
    )

    mentee_name = clean_value(
        match.get("mentee_name"),
        default="멘티"
    )

    mentee_dept = clean_value(
        match.get("mentee_dept")
    )

    mentee_grade = clean_value(
        match.get("mentee_grade")
    )

    result_type = clean_value(
        match.get("result_type")
    )
    
    topic = clean_value(
        match.get("topic")
    )
    
    preferred_field = clean_value(
        match.get("preferred_field")
    )
    
    question_text = match.get("question", "")
    
    main_question = clean_value(
        match.get("main_question")
    )
    
    if main_question == "-":
        main_question = extract_application_value(
            question_text,
            "핵심 질문 1:"
        )

    mentoring_method = clean_value(
        match.get("mentoring_method")
    )
    
    if mentoring_method == "-":
        mentoring_method = extract_application_value(
            question_text,
            "희망 방식:"
        )
    
    
    schedule_1 = clean_value(
        match.get("schedule_1")
    )
    
    if schedule_1 == "-":
        schedule_1 = extract_application_value(
            question_text,
            "1순위:"
        )
    
    
    schedule_2 = clean_value(
        match.get("schedule_2")
    )
    
    if schedule_2 == "-":
        schedule_2 = extract_application_value(
            question_text,
            "2순위:"
        )
    
    
    schedule_3 = clean_value(
        match.get("schedule_3")
    )
    
    if schedule_3 == "-":
        schedule_3 = extract_application_value(
            question_text,
            "3순위:"
        )

    

    accepted_schedule = clean_value(
        match.get("accepted_schedule")
    )


    with st.container(border=True):

        st.markdown("### 🔔 새로운 멘토링 요청")

        st.write(
            f"**[멘티]** {mentee_name} "
            f"({mentee_dept} / {mentee_grade})"
        )

        st.write(f"**[유형]** {topic}")
        st.write(f"**[희망 분야]** {preferred_field}")
        st.write(f"**[핵심 질문]** “{main_question}”")
        st.write(f"**[희망 방식]** {mentoring_method} (1순위: {schedule_1})")
        st.write(f"**[추천 유형]** {result_type}")
        st.write(f"**[현재 상태]** {get_status_text(status)}")


        with st.expander("📄 신청서 전체 내용 보기"):
            render_application_detail(
                match,
                mode="received"
            )


        # =========================================
        # pending
        # =========================================

        if status == "pending":

            st.warning("현재 상태: 수락 대기 중")

            c1, c2, c3 = st.columns(3)


            # -----------------------------
            # 1순위로 수락
            # -----------------------------

            with c1:

                if st.button(
                    f"1순위({schedule_1})로 수락",
                    key=f"accept_1_{match_id}",
                    use_container_width=True
                ):
                    st.session_state.accepting_match_id = match_id
                    st.session_state.accepting_schedule = schedule_1
                    st.rerun()

            # -----------------------------
            # 2순위로 수락
            # -----------------------------

            with c2:

                if st.button(
                    f"2순위({schedule_2})로 수락",
                    key=f"accept_2_{match_id}",
                    use_container_width=True
                ):
                    st.session_state.accepting_match_id = match_id
                    st.session_state.accepting_schedule = schedule_2
                    st.rerun()


            # -----------------------------
            # 거절
            # -----------------------------

            with c3:

                if st.button(
                    "거절",
                    key=f"reject_{match_id}",
                    use_container_width=True
                ):

                    try:

                        update_match_status(
                            match_id,
                            "rejected"
                        )

                        st.warning("매칭 신청을 거절했습니다.")
                        st.rerun()

                    except Exception as e:

                        st.error(
                            f"거절 처리 중 오류가 발생했습니다: {e}"
                        )


        if st.session_state.get("accepting_match_id") == match_id:


                selected_schedule = st.session_state.get("accepting_schedule", "-")
                openchat_link = get_mentor_openchat_link(match)
            
                st.divider()
                st.markdown("#### 🔐 오픈채팅방 비밀번호 입력")
            
                if openchat_link:
                    st.write(f"**오픈채팅방 링크:** {openchat_link}")
                else:
                    st.warning(
                        "멘토 등록 정보에 오픈채팅방 링크가 없습니다. "
                        "멘토 등록 페이지에서 링크를 먼저 입력해주세요."
                    )
            
                with st.form(f"openchat_password_form_{match_id}"):
            
                    openchat_password = st.text_input(
                        "오픈채팅방 비밀번호",
                        type="password",
                        placeholder="멘티에게 전달할 오픈채팅방 비밀번호를 입력해주세요."
                    )
            
                    col_ok, col_cancel = st.columns(2)
            
                    with col_ok:
                        submitted_password = st.form_submit_button(
                            "비밀번호 보내고 수락하기",
                            type="primary",
                            use_container_width=True
                        )
            
                    with col_cancel:
                        cancel_accept = st.form_submit_button(
                            "취소",
                            use_container_width=True
                        )
            
                if submitted_password:
            
                    if not openchat_link:
                        st.warning("오픈채팅방 링크를 먼저 등록해주세요.")
                        st.stop()
            
                    if not openchat_password.strip():
                        st.warning("오픈채팅방 비밀번호를 입력해주세요.")
                        st.stop()
            
                    try:
                        update_match_status(
                            match_id,
                            "accepted",
                            accepted_schedule=selected_schedule,
                            openchat_password=openchat_password.strip(),
                            openchat_link=openchat_link,
                        )
            
                        st.session_state.pop("accepting_match_id", None)
                        st.session_state.pop("accepting_schedule", None)
            
                        st.success("오픈채팅방 비밀번호를 전달하고 매칭을 수락했습니다.")
                        st.rerun()
            
                    except Exception as e:
                        st.error(f"수락 처리 중 오류가 발생했습니다: {e}")
            
                if cancel_accept:
                    st.session_state.pop("accepting_match_id", None)
                    st.session_state.pop("accepting_schedule", None)
                    st.rerun()


        # =========================================
        # accepted
        # =========================================

        elif status == "accepted":

            st.success("🟢 현재 상태: 수락 완료")

            if accepted_schedule and accepted_schedule != "-":
                st.write(f"**확정 일정:** {accepted_schedule}")


            openchat_link = clean_value(match.get("openchat_link"), default="")
            openchat_password = clean_value(match.get("openchat_password"), default="")
            
            if openchat_link:
                st.write(f"**오픈채팅방 링크:** {openchat_link}")
            
            if openchat_password:
                st.write(f"**전달한 비밀번호:** `{openchat_password}`")


        # =========================================
        # rejected
        # =========================================

        elif status == "rejected":

            st.error("🔴 현재 상태: 거절됨")


        st.divider()


# =========================================================
# 탭
# =========================================================

tab1, tab2 = st.tabs(
    [
        "내 신청 현황",
        "받은 신청",
    ]
)


# =========================================================
# 1. 내가 보낸 신청
# =========================================================

with tab1:

    st.subheader("내가 보낸 매칭 신청")

    try:

        sent_matches = get_sent_matches(user_id)

    except Exception as e:

        st.error(
            f"매칭 신청을 불러오는 중 오류가 발생했습니다: {e}"
        )

        sent_matches = []


    if not sent_matches:

        with st.container(border=True):

            st.info("아직 보낸 매칭 신청이 없습니다.")

            st.write(
                "멘토를 선택해 매칭을 신청하면 "
                "이곳에서 상태를 확인할 수 있어요."
            )

        if st.button(
            "홈으로 돌아가기",
            use_container_width=True,
            key="home_empty_sent"
        ):

            st.switch_page("app.py")


    else:

        for match in sent_matches:

            render_sent_match_card(match)


        if st.button(
            "홈으로 돌아가기",
            use_container_width=True,
            key="home_sent"
        ):

            st.switch_page("app.py")


# =========================================================
# 2. 내가 받은 신청
# =========================================================

with tab2:

    st.subheader("내게 온 매칭 신청")

    try:

        received_matches = get_received_matches(user_id)

    except Exception as e:

        st.error(
            f"받은 매칭 신청을 불러오는 중 오류가 발생했습니다: {e}"
        )

        received_matches = []


    if not received_matches:

        with st.container(border=True):

            st.info("아직 받은 매칭 신청이 없습니다.")

            st.write(
                "후배가 매칭을 신청하면 "
                "이곳에서 수락하거나 거절할 수 있어요."
            )


    else:

        for match in received_matches:

            render_received_match_card(match)


render_footer()
