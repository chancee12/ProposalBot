import utils
import streamlit as st
from streaming import StreamHandler

from langchain.llms import OpenAI
from langchain.chains import ConversationChain

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

    st.set_page_config(page_title="Chatbot", page_icon="💬")
    st.header('Basic Chatbot')
    st.write('Allows users to interact with the LLM')

    class Basic:

        def __init__(self):
            utils.configure_openai_api_key()
            self.openai_model = st.selectbox('Select LLM model', ('gpt-4', 'gpt-3.5-turbo'))

        def setup_chain(self):
            llm = OpenAI(model_name=self.openai_model, temperature=0, streaming=True)
            chain = ConversationChain(llm=llm, verbose=True)
            return chain
        
        @utils.enable_chat_history
        def main(self):
            chain = self.setup_chain()
            user_query = st.chat_input(placeholder="Ask me anything!")
            if user_query:
                utils.display_msg(user_query, 'user')
                with st.chat_message("assistant"):
                    st_cb = StreamHandler(st.empty())
                    response = chain.run(user_query, callbacks=[st_cb])
                    st.session_state.messages.append({"role": "assistant", "content": response})

    if __name__ == "__main__":
        obj = Basic()
        obj.main()
