"""채팅 데이터 접근 계층 (Supabase)"""
from utils.supabase_client import get_client


def can_access_conversation(conversation_id: str, user_id: str) -> bool:
    """사용자가 해당 채팅방 참여자인지 권한 확인"""
    sb = get_client()
    res = (
        sb.table("conversations")
        .select("mentor_id, mentee_id")
        .eq("id", conversation_id)
        .single()
        .execute()
    )
    if not res.data:
        return False
    return user_id in (res.data["mentor_id"], res.data["mentee_id"])


def get_my_conversations(user_id: str) -> list:
    """내가 참여한 채팅방 목록 (상대방 이름 포함)"""
    sb = get_client()
    res = (
        sb.table("conversations")
        .select("id, mentor_id, mentee_id, "
                "mentor:profiles!conversations_mentor_id_fkey(name), "
                "mentee:profiles!conversations_mentee_id_fkey(name)")
        .or_(f"mentor_id.eq.{user_id},mentee_id.eq.{user_id}")
        .order("created_at", desc=True)
        .execute()
    )
    convs = []
    for c in res.data or []:
        if c["mentor_id"] == user_id:
            partner = (c.get("mentee") or {}).get("name", "멘티")
        else:
            partner = (c.get("mentor") or {}).get("name", "멘토")
        convs.append({"id": c["id"], "partner_name": partner})
    return convs


def create_conversation_if_accepted(mentor_id: str, mentee_id: str):
    """매칭 수락된 경우에만 채팅방 생성. 이미 있으면 기존 방 반환."""
    sb = get_client()
    # 매칭 수락 여부 확인
    match = (
        sb.table("matches")
        .select("status")
        .eq("mentor_id", mentor_id)
        .eq("mentee_id", mentee_id)
        .eq("status", "accepted")
        .execute()
    )
    if not match.data:
        return None, "매칭이 수락되지 않아 채팅을 시작할 수 없습니다."

    existing = (
        sb.table("conversations")
        .select("id")
        .eq("mentor_id", mentor_id)
        .eq("mentee_id", mentee_id)
        .execute()
    )
    if existing.data:
        return existing.data[0]["id"], None

    created = (
        sb.table("conversations")
        .insert({"mentor_id": mentor_id, "mentee_id": mentee_id})
        .execute()
    )
    return created.data[0]["id"], None


def get_messages(conversation_id: str) -> list:
    """메시지를 시간순으로 조회"""
    sb = get_client()
    res = (
        sb.table("messages")
        .select("id, conversation_id, sender_id, content, created_at, is_read, "
                "sender:profiles(name)")
        .eq("conversation_id", conversation_id)
        .order("created_at", desc=False)
        .execute()
    )
    msgs = []
    for m in res.data or []:
        m["sender_name"] = (m.get("sender") or {}).get("name", "")
        msgs.append(m)
    return msgs


def send_message(conversation_id: str, sender_id: str, content: str):
    """메시지 DB insert"""
    sb = get_client()
    sb.table("messages").insert({
        "conversation_id": conversation_id,
        "sender_id": sender_id,
        "content": content,
    }).execute()


def mark_as_read(conversation_id: str, reader_id: str):
    """상대가 보낸 메시지를 읽음 처리"""
    sb = get_client()
    sb.table("messages").update({"is_read": True}) \
        .eq("conversation_id", conversation_id) \
        .neq("sender_id", reader_id) \
        .eq("is_read", False) \
        .execute()
