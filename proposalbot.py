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
    st.title("Axim's GIS Government Proposal Assistant Beta V.1.0.3")
    st.markdown(
        """
        Welcome to Axim's GIS Government Proposal Assistant! This AI assistant, powered by GPT-4, has been designed to provide invaluable support during the government contracting proposal process. The AI assistant excels in:
        * Restructuring sentences for improved readability
        * Clarifying ambiguities and eliminating unnecessary redundancies
        * Summarizing key points of lengthy texts
        * Identifying key proposal requirements and potential areas of improvement
        * Creating and deduplicating acronym lists
        * Generating responses to common GIS-related RFP questions
        In addition, the assistant is equipped with a deep understanding of GIS concepts and government contracting specifics, ensuring that you have a dedicated, knowledgeable tool at your disposal for proposal revision and optimization.
        """
    )

    openai.api_key = st.secrets["OPENAI_API_KEY"]

    MODEL = "gpt-4"
    
    llm = OpenAI(
        temperature=0,
        openai_api_key=openai.api_key,
        model_name=MODEL,
        verbose=False
    )

    if 'entity_memory' not in st.session_state:
            st.session_state.entity_memory = ConversationEntityMemory(llm=llm, k=100 )

    task_options = [
        "Custom Prompt",
        "Create Acronym List",
        "Identify Key Proposal Requirements",
        "Summarize GIS Service Description",
        "Simplify Complex GIS Language",
        "Summarize Proposal Section",
        "Revise Proposal Text",
        "Identify Improvement Areas",
        "Respond to RFP Questions",
        "Analyze Technical Requirements"
    ]
    selected_task = st.selectbox("Select a task:", task_options)

    user_input = st.text_area("Type or paste your text here:", "")

    if user_input:
        prompt_mapping = {
            # Replace with extensive prompt for each task
            "Custom Prompt": user_input,
            "Create Acronym List": f"{user_input} - extract and deduplicate acronyms",
            "Identify Key Proposal Requirements": f"{user_input} - identify key requirements",
            # and so on for all the tasks...
        }

        Conversation = ConversationChain(
            llm=llm, 
            prompt=prompt_mapping[selected_task],
            memory=st.session_state.entity_memory
        )

        output = Conversation(user_input)
        st.text_area("AI's response:", output)
