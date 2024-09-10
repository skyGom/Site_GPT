import streamlit as st

def init_session_state_message():
    st.session_state["message"] = []

def paint_message(message, role, is_save=True):
    with st.chat_message(role):
        st.markdown(message)
        
    if is_save:
        st.session_state["message"].append({"message": message, "role": role})
        
def paint_message_history():
    for message in st.session_state["message"]:
        paint_message(message["message"], message["role"])