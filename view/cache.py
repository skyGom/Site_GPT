import streamlit as st

from gpt.retriever import get_retriever_after_embedding

from datetime import timedelta

@st.cache_data(show_spinner="Loading website...")
def get_cached_retirever_after_embedding(url, api_key):
    return get_retriever_after_embedding(url, api_key)