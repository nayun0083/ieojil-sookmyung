from supabase import create_client, Client
import streamlit as st


def get_client() -> Client:
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY"].strip()

    url = url.replace("/rest/v1", "")
    url = url.replace("/auth/v1", "")
    url = url.rstrip("/")

    sb = create_client(url, key)

    access_token = st.session_state.get("sb_access_token")
    refresh_token = st.session_state.get("sb_refresh_token")

    if access_token and refresh_token:
        try:
            sb.auth.set_session(access_token, refresh_token)
        except Exception:
            pass

    return sb
