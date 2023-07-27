import streamlit as st
from PIL import Image
import openai
import time
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
import re

def is_four_digit_number(string):
    pattern = r'^\d{4}$'  # Matches exactly four digits
    return bool(re.match(pattern, string))

def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False
    if "password_correct" not in st.session_state:
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        return True

if check_password():
    st.set_page_config(layout="wide")

    st.sidebar.title("Contact")
    st.sidebar.info(
        """
        Chancee Vincent:
        [LinkedIn](www.linkedin.com/in/chancee-vincent-4371651b6)
        """
    )
    st.title("Chancee's Proposal Chatbot Beta V.1.0.3")
    st.markdown(
        """
        This AI assistant is designed specifically to revise government contracting proposals. Utilizing GPT-3, it assists in:
        * Restructuring sentences for improved readability
        * Clarifying ambiguities
        * Eliminating unnecessary redundancies
        * Enhancing the overall presentation
        """
    )

    openai.api_key = st.secrets["OPENAI_API_KEY"]

    MODEL = st.selectbox("Choose model", ("text-davinci-003", "gpt-4"))
    
    llm = OpenAI(
        temperature=0,
        openai_api_key=openai.api_key,
        model_name=MODEL,
        verbose=False
    )

    if 'entity_memory' not in st.session_state:
            st.session_state.entity_memory = ConversationEntityMemory(llm=llm, k=100 )

    Conversation = ConversationChain(
            llm=llm, 
            prompt="",
            memory=st.session_state.entity_memory
    )

    user_input = st.text_area("Type your question:", "")

    if user_input:
        output = Conversation(user_input)
        st.text_area("Bot's answer:", output)
