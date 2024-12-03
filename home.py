import streamlit as st
import yaml

with open('./data/home.yml', 'r') as file:
    content = yaml.safe_load(file)['home']

st.title("CUHK DIIR Case Simulation Chatbot Demo")
st.subheader("Description")
st.image("./data/imgs/chatbot-concept-overview.jpg", width=512)
st.markdown(content["description"])
st.subheader("Instructions")
st.markdown(content["instructions"])
st.subheader("Acknowledgments")
st.markdown(content["acknowledgments"])
