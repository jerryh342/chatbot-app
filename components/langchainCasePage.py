import time
import streamlit as st

from langchain_core.messages import RemoveMessage
from langchain_core.messages.ai import AIMessageChunk
from langchain_core.messages.human import HumanMessage

from .casePage import CasePage
from schema.schema import Case


class LangChainCasePage(CasePage):
    def __init__(self, case: Case):
        super().__init__(case)
        self.config = {
            "configurable": {
                "thread_id": "abc123",
            }
        }
        graph = st.session_state.graph
        chat_history = graph.get_state(self.config).values["messages"]
        for message in chat_history:
            message.pretty_print()

    def clearConversation(self) -> None:
        chat_history = st.session_state.graph.get_state(self.config).values["messages"]
        st.session_state.graph.update_state(config=self.config, values={
                                            "messages": [RemoveMessage(id=m.id) for m in chat_history[1:]]})
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi, I'm Dr.XRLiA. You can submit your answers for this case to me and I'll evaluate them! \n Feel free to ask me questions related to lines and tubes on CXRs as well."}]

    def getMessageContent(self, generator):
        for chunk in generator:
            # chunk is tuple(MessageChunk, dict(model_params))
            print(type(chunk[0]), type(chunk[1]))
            time.sleep(0.05)
            if isinstance(chunk[0], AIMessageChunk):
                yield chunk[0].content

    def onSubmitNewPrompt(self, prompt: str = "", showUserPrompt: bool = True) -> None:
        if prompt == "":
            prompt = st.session_state.chatInput
        if showUserPrompt:
            self.updateChatHistory(role="user", content=prompt)
        with self.chatContainer:
            if showUserPrompt:
                with st.chat_message("user"):
                    st.markdown(prompt)
            with st.chat_message("assistant"):
                response = st.write_stream(self.getMessageContent(st.session_state.graph.stream(
                    {"messages": [HumanMessage(prompt)]}, config=self.config, stream_mode="messages")))
            # response = st.session_state.graph.invoke(
            # {"messages": [HumanMessage(prompt)]}, config=self.config)
        self.updateChatHistory(role="assistant", content=response)

    def onSubmitScenarioForm(self) -> None:
        prefix = f"case{self.currentCase.caseNum}Question"
        prompt = f"Stage {st.session_state.currentStage} \n"
        for idx, key in enumerate(sorted([key for key in st.session_state.keys() if prefix in key])):
            question = self.currentCase.questions[f'stage{st.session_state.currentStage}'][idx]['question']
            answer = self.currentCase.questions[f'stage{st.session_state.currentStage}'][idx]['answer']
            result = f"Question {idx + 1}: {question}\nCorrect answer: {answer}\nUser answer: {st.session_state[key]}\n\n"
            prompt += result
        prompt += f"Evaluate the above questions as instructed in system message, with reference to context from case {self.currentCase.caseNum}."
        self.onSubmitNewPrompt(prompt, False)
        st.session_state.currentStage = st.session_state.currentStage + 1
        print(f"casePage script: {st.session_state.currentStage}")
