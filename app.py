import streamlit as st

from gpt.model import create_llm, is_valid_openai_key
from gpt.chain import create_chain

from view.cache import get_cached_retirever_after_embedding
from view.message import init_session_state_message, paint_message, paint_message_history

from utility.url import ensure_sitemap_url

if "messages" not in st.session_state:
    init_session_state_message()

st.set_page_config(page_title="Site_GPT", page_icon="🗺️",)

st.title("Site_GPT")

st.markdown(
    """
    # SiteGPT
            
    Ask questions about the content of a website.
            
    Start by writing the URL of the website on the sidebar.
"""
)

if "api_key" not in st.session_state:
    st.session_state.api_key = None

with st.sidebar:
    if st.session_state.api_key is None:
        api_key = st.text_input("First write down OpenAI API key.", type="password")
        
        if api_key:
            with st.spinner("Checking API Key..."):
                if is_valid_openai_key(api_key):
                    st.session_state.api_key = api_key
                else:
                    st.warning("API key is not valid. Try again.")
    
    url = st.text_input("Write down a URL", placeholder="https://www.example.com/sitemap.xml")
    st.link_button("Git repository", "https://platform.openai.com/account/api-keys")
    
if url and st.session_state["api_key"]:
    llm = create_llm(st.session_state.api_key)
    url = ensure_sitemap_url(url)
    retriever = get_cached_retirever_after_embedding(url, st.session_state.api_key)
        
    if len(st.session_state["messages"]) <= 0:
        paint_message("", "ai")
    paint_message_history()
        
    input_answer = st.text_input("Ask a question to the website", placeholder="What is the website about?")
    if input_answer:
        paint_message(input_answer, "You")
        with st.spinner("Thinking..."):
            chain = create_chain(retriever, llm)
            with st.chat_message("ai"):
                response = chain.invoke(input_answer)
    else:
        init_session_state_message()