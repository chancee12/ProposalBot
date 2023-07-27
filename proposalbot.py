import streamlit as st
from PIL import Image
import openai
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts.prompt import PromptTemplate
import re

# Configure the layout at the very beginning
st.set_page_config(layout="wide")

prompt_mapping = {
            "Custom Prompt": user_input,
            "Create Acronym List": f"Please create a deduplicated list of acronyms from the following text: '{user_input}'",
            "Identify Key Proposal Requirements": f"Identify key requirements from the following proposal text: '{user_input}'",
            "Summarize GIS Service Description": f"Provide a concise summary of the following GIS service description: '{user_input}'",
            "Simplify Complex GIS Language": f"Simplify the following complex GIS-related language for a non-technical audience: '{user_input}'",
            "Summarize Proposal Section": f"Provide a brief summary of the following proposal section: '{user_input}'",
            "Revise Proposal Text": f"Revise the following proposal text for improved clarity and effectiveness: '{user_input}'",
            "Identify Improvement Areas": f"Identify potential areas for improvement in the following proposal text: '{user_input}'",
            "Respond to RFP Questions": f"Generate a response to the following GIS-related RFP question: '{user_input}'",
            "Analyze Technical Requirements": f"Analyze the following technical requirements and provide an evaluation: '{user_input}'"
        }

def is_four_digit_number(string):
    pattern = r'^\d{4}$'
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

openai.api_key = st.secrets["OPENAI_API_KEY"]
models = ["gpt-4", "text-davinci-003"]
selected_model = st.sidebar.selectbox("Select a model (GPT-4 is default and preferred for most tasks. text-davinci-003 is an older model and may not perform as well):", models, index=0, key="model_selection")

# Initialize OpenAI object
llm = OpenAI(
    temperature=0,
    openai_api_key=openai.api_key,
    model_name=selected_model,
    verbose=False
)

# Initialize ConversationBufferMemory object
if 'entity_memory' not in st.session_state:
    st.session_state.entity_memory = ConversationBufferMemory(
        llm=llm, 
        ai_prefix="AI",
        human_prefix="User",
    )

# Define the prompt template and create a ConversationChain object
prompt_template = """
Current conversation:
{history}
User: {input}
AI:"""
PROMPT = PromptTemplate(input_variables=["history", "input"], template=prompt_template)
Conversation = ConversationChain(
    llm=llm,
    prompt=PROMPT,
    memory=st.session_state.entity_memory,
)

# Ensures 'selected_task' exists in session state
if 'selected_task' not in st.session_state:
    st.session_state['selected_task'] = ''

# Then it's safe to use st.session_state['selected_task'] in your prompt_mapping
prompt_to_use = ""  # default value
if st.session_state.selected_task in prompt_mapping:
    prompt_to_use = prompt_mapping[st.session_state.selected_task]

def on_input_change():
    user_input = st.session_state.user_input
    st.session_state.past.append(user_input)
    if user_input:
        if is_four_digit_number(user_input):
            st.error("😕 Please enter more than four digits.")
            return

        if st.session_state.selected_task in prompt_mapping:
            prompt_to_use = prompt_mapping[st.session_state.selected_task].format(input=user_input)

        Conversation = ConversationChain(
            llm=llm, 
            memory=st.session_state.entity_memory
        )
        output = Conversation.predict(prompt_to_use)
        st.session_state.conversation_history += f"\nUser: {user_input}\nAI: {output}"
        st.session_state.generated.append(f"AI: {output}")
    st.session_state.user_input = ''

def on_btn_click():
    del st.session_state.past[:]
    del st.session_state.generated[:]

if check_password():

    st.sidebar.title("Contact")
    st.sidebar.info(
        """
        Chancee Vincent:
        [LinkedIn](https://www.linkedin.com/in/chancee-vincent-4371651b6)
        """
    )
    st.title("Chancee's GIS Government Proposal Assistant Beta V.1.0.4")
    st.markdown(
        """
        Welcome to Chancee's GIS Government Proposal Assistant for Axim! This AI assistant, powered by GPT-4, has been designed to provide invaluable support during the government contracting proposal process. The AI assistant excels in:
        * Restructuring sentences for improved readability
        * Clarifying ambiguities and eliminating unnecessary redundancies
        * Summarizing key points of lengthy texts
        * Identifying key proposal requirements and potential areas of improvement
        * Creating and deduplicating acronym lists
        * Generating responses to common GIS-related RFP questions
        In addition, the assistant is equipped with a deep understanding of GIS concepts and government contracting specifics, ensuring that you have a dedicated, knowledgeable tool at your disposal for proposal revision and optimization.
        """
    )

    if 'entity_memory' not in st.session_state:
        st.session_state.entity_memory = ConversationEntityMemory(llm=llm, k=100 )

    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = ""

    if 'past' not in st.session_state:
        st.session_state.past = []
        
    if 'generated' not in st.session_state:
        st.session_state.generated = []
        
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ''

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

    selected_task = st.selectbox("Select a task:", task_options, index=0, key='task_selection')

    def display_chat():
        for i in range(len(st.session_state['past'])):
            st.markdown(f"**User**: {st.session_state['past'][i]}")
            if i < len(st.session_state['generated']):
                st.markdown(f"**AI**: {st.session_state['generated'][i]}")

    if check_password():
        with st.form(key="form"):
            user_input = st.text_input("User Input:", key="user_input")
            submit_button = st.form_submit_button("Submit")

            if submit_button:
                on_input_change()

        display_chat()

        st.button("Clear message", on_click=on_btn_click)

