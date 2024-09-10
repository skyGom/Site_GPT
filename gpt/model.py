from langchain.chat_models import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler

from view.message import paint_message

import openai

import streamlit as st

def create_llm(key):
    return ChatOpenAI(
        temperature=0.1,
        model="gpt-4o-mini-2024-07-18",
        streaming=True,
        callbacks=[_ChatCallbackHandler()],
        api_key=key,
    )
    
def is_valid_openai_key(key):
    try:
        openai.api_key = key
        openai.Model.list()
        return True
    except Exception as e:
        return False
    
class _ChatCallbackHandler(BaseCallbackHandler):
    message = ""
    
    def on_llm_start(self, *args, **kwargs):
        self.message_box = st.empty()
            
    def on_llm_end(self, *arg, **kwargs):
        paint_message(self.message, "ai")
            
    def on_llm_new_token(self, token, *arg, **kwargs):
        self.message += token
        self.message_box.markdown(self.message)