import streamlit as st

def render_message(msg: dict, my_user_id: str):
    """내 메시지는 오른쪽 정렬, 상대는 왼쪽 정렬"""
    is_mine = msg["sender_id"] == my_user_id
    align = "flex-end" if is_mine else "flex-start"
    bg = "#F8BBD0" if is_mine else "#F1F1F1"
    name = "나" if is_mine else msg.get("sender_name", "상대")
    time = str(msg.get("created_at", ""))[11:16]

    st.markdown(
        f"""
        <div style="display:flex; justify-content:{align}; margin:6px 0;">
            <div style="max-width:70%;">
                <div style="font-size:11px; color:#999; text-align:{'right' if is_mine else 'left'};">
                    {name} · {time}
                </div>
                <div style="background:{bg}; padding:8px 12px; border-radius:12px;
                            display:inline-block; word-break:break-word;">
                    {msg['content']}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
