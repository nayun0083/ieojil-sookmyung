from supabase import create_client, Client
import streamlit as st


def get_client() -> Client:
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY"].strip()

    # Supabase 화면에서 /rest/v1까지 복사한 경우를 대비해 자동 제거
    url = url.replace("/rest/v1", "")
    url = url.replace("/auth/v1", "")
    url = url.rstrip("/")

    return create_client(url, key)