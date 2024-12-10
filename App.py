import glob

import streamlit as st

from components.server import getNewConversationID

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm Dr.ChestXpert. You can submit your answers for this case to me and I'll evaluate them! \n Feel free to ask me questions related to lines and tubes on CXRs as well."}]

if "currentStage" not in st.session_state:
    st.session_state.currentStage = 1

if "currentCase" not in st.session_state:
    st.session_state.currentCase = 0

if 'sessionID' not in st.session_state:
    st.session_state.sessionID = 2514216  # getNewConversationID()

# Set up pages and navigation
homePage = st.Page("home.py", title="Home")
pages = [homePage]

casePaths = sorted(glob.glob("./cases/*.py"))
for idx, casePath in enumerate(casePaths):
    page = st.Page(casePath, title=f"Case {idx+1}")
    pages.append(page)

pg = st.navigation(pages)

# Page config
st.set_page_config(page_title="DIIR Chatbot Demo", layout="wide", page_icon="./data/logo.jpg")
st.html('<head><link rel="apple-touch-icon" href="https: // cuhkdri-chatbotapp.streamlit.app: 443/~/+/media/5f1edb7658699eb9c2d9cb7fb91b11e11d6a7e7211db272456a1a3c8.jpg" /></head>')
st.logo("./data/logo.jpg", size="large")
pg.run()
