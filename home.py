import streamlit as st

st.title("CUHK DIIR Case Simulation Chatbot Demo")
st.subheader("Description")
st.image("./data/imgs/chatbot-concept-overview.jpg", width=512)
st.markdown("We propose a chatbot-integrated case simulation to enhance students' understanding on lines and tubes in radiology based on active learning principles.  \n Students will be briefed with the case and asked to answer case-specific questions drafted by radiologists, and the chatbot will act as a personal tutor to provide a personalized evaluation of the students' performances.  \n We expect that this can enhance the learning experience and make case simulations a more accessible exercise for students.")
st.subheader("Instructions")
st.markdown("- Select a case and read through the background  \n- Answer questions by filling in the text box with your own box  \n- Submit your answers and review the chatbot's evaluation  \n- Engage in follow-up discussion or a question set with increased difficulty")
st.subheader("Acknowledgments")
st.markdown("This project was supported by the *University Grants Committee (UGC) Teaching Development and Language Enhancement Grant 2022-25*.  \n We have no other conflicts of interest to disclose.")
