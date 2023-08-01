import streamlit as st

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

With Langchain, we have significantly simplified chatbot creation. Here are several examples of chatbot implementations serving different needs:

- **Basic Chatbot**: Facilitates interactive conversations with the LLM.
- **Context-aware Chatbot**: A chatbot capable of retaining past conversation context to produce more relevant responses.
- **Internet-Accessible Chatbot**: This chatbot can access the internet to answer user inquiries about current events.
- **Document-Integrated Chatbot**: This chatbot has the ability to reference custom documents, enabling it to respond to user queries with information from specific documents.

To explore the functionality of each chatbot, please navigate to the respective chatbot section.
""")
