import glob

import streamlit as st
from langchain_core.messages.system import SystemMessage

from chatbot.graph import build_graph
# page config
st.set_page_config(page_title="DIIR Chatbot Demo", layout="wide")

# Initialize session state variables
graph = build_graph()
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm Dr.XRLiA. You can submit your answers for this case to me and I'll evaluate them! \n Feel free to ask me questions related to lines and tubes on CXRs as well."}]

if "currentStage" not in st.session_state:
    st.session_state.currentStage = 1

if "currentCase" not in st.session_state:
    st.session_state.currentCase = 0

if 'sessionID' not in st.session_state:
    st.session_state.sessionID = 2514216  # getNewConversationID()

if 'lcConfig' not in st.session_state:
    st.session_state.lcConfig = {"configurable": {"thread_id": "abc123"}}

if "graph" not in st.session_state:
    st.session_state.graph = graph
    with open("./data/prompts/sysprompt.txt", "r") as f:
        sys_prompt = f.read()
    # system_msg = SystemMessage(sys_prompt)
    system_msg = SystemMessage(sys_prompt)
    st.session_state.graph.update_state(config=st.session_state.lcConfig, values={"messages": [system_msg]})

# Set up pages and navigation
homePage = st.Page("home.py", title="Home")
# lcChatPage = st.Page("./utils/langchainChat.py", title="LangChain Chatbot")
# pages = [homePage, lcChatPage]
pages = [homePage]

casePaths = sorted(glob.glob("./cases/*.py"))
for idx, casePath in enumerate(casePaths):
    page = st.Page(casePath, title=f"Game {idx+1}")
    pages.append(page)

# pages.append(st.Page("./components/embedding.py", title="Embedding"))
# Page config

pg = st.navigation(pages)

pg.run()
