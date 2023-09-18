import utils
import streamlit as st
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentType, initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun
from langchain.callbacks import StreamlitCallbackHandler

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

    st.set_page_config(page_title="ChatWeb", page_icon="🌐")
    st.header('Chatbot with Internet Access')
    st.write('Equipped with internet access, enables users to ask questions about recent events')

    class ChatbotTools:

        def __init__(self):
            utils.configure_openai_api_key()
            self.openai_model = st.selectbox('Select LLM model', ('gpt-4', 'gpt-3.5-turbo'))
            self.memory = ConversationBufferMemory()  # Initialize memory object

        def setup_agent(self):
            # Define tool
            ddg_search = DuckDuckGoSearchRun()
            tools = [
                Tool(
                    name="DuckDuckGoSearch",
                    func=ddg_search.run,
                    description="Useful for when you need to answer questions about current events. You should ask targeted questions",
                )
            ]

            # Setup LLM and Agent
            llm = ChatOpenAI(model_name=self.openai_model, streaming=True)
            chain = ConversationChain(llm=llm, memory=self.memory, verbose=True)  # Include memory object in chain setup
            agent = initialize_agent(
                tools=tools,
                llm=chain,  # Modify this to include the chain object instead of llm
                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                handle_parsing_errors=True,
                verbose=True
            )
            return agent

        @utils.enable_chat_history
        def main(self):
            agent = self.setup_agent()
            user_query = st.chat_input(placeholder="Ask me anything!")
            if user_query:
                utils.display_msg(user_query, 'user')
                with st.chat_message("assistant"):
                    st_cb = StreamlitCallbackHandler(st.container())
                    response = agent.run(user_query, callbacks=[st_cb])
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.write(response)

    if __name__ == "__main__":
        obj = ChatbotTools()
        obj.main()  # This line calls the main method, which will display the input box
