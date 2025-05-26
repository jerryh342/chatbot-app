import os
import random
import time

import streamlit as st

from components.server import updateConversation
from schema.schema import Case


class CasePage():
    def __init__(self, case: Case) -> None:
        self.currentCase = case  # Update current case number
        st.title(f"Game {self.currentCase.caseNum}")
        self.bgTab, self.questionsTab, self.imagesTab = st.tabs(["Background", "Questions", "CXR Images"])
        with self.bgTab:
            st.markdown(case.caseDesc)
        with self.questionsTab:
            # st.session_state.currentStage = st.slider(
            # "Stage Selector", min_value=1, max_value=case.maxStage+1, step=1, )
            # button = st.button('add stage', 'nextStageBtn', on_click=self.addStage)
            # Stage progression by conditional rendering of form
            if (st.session_state.currentStage <= case.maxStage):
                self.scenarioCol, self.chatbotCol = st.columns([0.5, 0.5])
                with self.scenarioCol:
                    col1, col2 = st.columns([0.7, 0.3])
                    with col1:
                        st.markdown("**Questions to think about**")
                        st.write(f"Stage {st.session_state.currentStage}")
                    with col2:
                        st.button("Clear All Answers", "clearAnswersBtn", on_click=self.clearAllAnswers)
                    stageKey = f'stage{st.session_state.currentStage}'
                    self.loadScenarioForm(caseNum=case.caseNum, questions=case.questions[stageKey])
                with self.chatbotCol:
                    col1, col2 = st.columns([0.7, 0.3])
                    with col1:
                        st.markdown("**Talk to Dr. XRLiA**")
                    with col2:
                        st.button("Clear Conversation", "clearConversationBtn", on_click=self.clearConversation)
                    self.chatContainer = st.container(height=520, border=True)
                    self.loadConvoWindow()
            else:
                st.markdown("**Talk to Dr. XRLiA**")
                st.button("Clear Conversation", "clearConversationBtn", on_click=self.clearConversation)
                self.chatContainer = st.container(height=520, border=True)
                self.loadConvoWindow()
            with self.imagesTab:
                col1, col2 = st.columns([0.5, 0.5])
                with col1:
                    st.image("./data/cases/imgs/cxr-ett-normal.png", caption="Normal ETT", width=512)
                    st.markdown(
                        'Benzocaine-Induced Cyanosis - Scientific Figure on ResearchGate. Available from: https://www.researchgate.net/figure/A-chest-x-ray-showing-correct-endotracheal-tube-placement-and-no-acute-lung-pathology_fig2_303797877 [accessed 10 Dec 2024]')
                with col2:
                    st.image("./data/cases/imgs/cxr-ett-abnormal.png",
                             caption=["Abnormal ETT, tip in right main bronchus; Endotracheal tube: red dotted line; Trachea: blue dotted line; Nasogastric tube: yellow dotted line"], width=512)
                    st.html('Case courtesy of Frank Gaillard, <a href="https://radiopaedia.org/?lang=us">Radiopaedia.org</a>. From the case <a href="https://radiopaedia.org/cases/15330?lang=us">rID: 15330</a>')

    def loadScenarioForm(self, caseNum: int, questions: list):
        with st.form(key=f"case{caseNum}Form"):
            for idx, item in enumerate(questions):
                st.text_area(label=f"Question {idx+1}: {item['question']}", key=f"case{caseNum}Question{idx+1}")
            st.form_submit_button(on_click=self.onSubmitScenarioForm)
        return None

    def loadConvoWindow(self) -> None:
        with self.chatContainer:
            for message in st.session_state.messages:
                with st.chat_message(message['role']):
                    st.markdown(message['content'])
        st.chat_input("Ask me a question", key="chatInput", on_submit=self.onSubmitNewPrompt)

    def updateChatHistory(self, role: str, content: str) -> None:
        st.session_state.messages.append({
            "role": role,
            "content": content,
        })
        # print(f"updated chat history {role}, {content}")

    def onSubmitNewPrompt(self) -> None:
        prompt = st.session_state.chatInput
        self.updateChatHistory(role="user", content=prompt)
        with self.chatContainer:
            with st.chat_message("user"):
                st.markdown(prompt)
        with self.chatContainer:
            with st.chat_message("assistant"):
                response = st.write_stream(updateConversation(prompt))
                self.updateChatHistory(role="assistant", content=response)

    def onSubmitScenarioForm(self) -> None:
        prefix = f"case{self.currentCase.caseNum}Question"
        prompt = f"Part {st.session_state.currentStage} \n"
        for idx, key in enumerate(sorted([key for key in st.session_state.keys() if prefix in key])):
            question = self.currentCase.questions[f'stage{st.session_state.currentStage}'][idx]['question']
            answer = self.currentCase.questions[f'stage{st.session_state.currentStage}'][idx]['answer']
            result = f"Question {idx + 1}: {question}\nCorrect answer: {answer}\nUser answer: {st.session_state[key]}\n\n"
            prompt += result
        prompt += f"Evaluate the above questions as instructed in system message, with reference to context from case {self.currentCase.caseNum}."
        with self.chatContainer:
            with st.chat_message("assistant"):
                response = st.write_stream(updateConversation(prompt))
                self.updateChatHistory(role="assistant", content=response)
        st.session_state.currentStage = st.session_state.currentStage + 1
        print(f"casePage script: {st.session_state.currentStage}")

    def clearAllAnswers(self) -> None:
        prefix = f"case{self.currentCase.caseNum}Question"
        for key in sorted([key for key in st.session_state.keys() if prefix in key]):
            st.session_state[key] = ""

    def clearConversation(self) -> None:
        # st.session_state.sessionID =
        st.session_state.sessionID = 2514216  # getNewConversationID()
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi, I'm Dr. ChestXpert. You can submit your answers for this case to me, and I'll evaluate how well you did! I can also answer questions related to lines and tubes on CXRs as well."}]

    def addStage(self):
        st.session_state.currentStage += 1
        print(st.session_state.currentStage)
