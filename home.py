import streamlit as st

def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    st.set_page_config(
        page_title="Langchain Chatbot",
        page_icon='💬',
        layout='wide'
    )

    st.header("Exploring LLM's for Potential Axim Use by Chancee")
    st.sidebar.title("Contact")
    st.sidebar.info(
        """
        Chancee Vincent:
        [LinkedIn](https://www.linkedin.com/in/chancee-vincent-4371651b6)
        """
    )


    st.write("""
    Langchain is an effective framework conceived to expedite the development of applications powered by Language Models (LLMs). This open-source model delivers a well-rounded integration of diverse components, thereby streamlining the assembly process for robust application creation.

    One notable feature of this application is the ability for users to choose between GPT-3.5 and GPT-4 when interfacing with the chatbot. GPT-3.5 is a powerful language model capable of producing detailed, contextually relevant responses. However, for more complex tasks or inquiries, GPT-4 provides an advanced, more comprehensive language model that can generate even more sophisticated and nuanced responses.

    With Langchain, chatbot creation is simple. Here are several examples of chatbot implementations serving different needs:

    - **Basic Chatbot**: Facilitates interactive conversations with the LLM.
    - **Context-aware Chatbot**: A chatbot capable of retaining past conversation context to produce more relevant responses.
    - **Internet-Accessible Chatbot**: This chatbot can access the internet to answer user inquiries about current events.
    - **Document-Integrated Chatbot**: This chatbot has the ability to reference custom documents, enabling it to respond to user queries with information from specific documents.

    To explore the functionality of each chatbot, please navigate to the respective chatbot section.
    """)
