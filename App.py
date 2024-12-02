from dotenv import load_dotenv
import streamlit as st

from components.server import getNewConversationID
# Load env file
load_dotenv("chatbot.env")
st.set_page_config(page_title="DIIR Chatbot Demo", layout="wide")
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
    # st.session_state.sessionID = 2514216

# Homepage design
st.title("Case Simulation Chatbot Demo")
st.markdown("CUHK DIIR")
st.subheader("Description")
st.markdown("Description on the app; Current web app for DEMO purposes only")
st.subheader("Instructions")
st.markdown("Instructions on how to use the app")
st.subheader("Acknowledgments")
st.markdown("Acknowledgments")
