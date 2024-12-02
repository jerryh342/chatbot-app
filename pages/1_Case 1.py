import yaml
import streamlit as st
from components.casePage import CasePage
from schema.schema import Case

with open('C:\\Users\\Jerry H\\Desktop\\chatbot-app\\data\\cases\\case1.yml', 'r') as file:
    currentCaseYml = yaml.safe_load(file)['case']
if st.session_state.currentCase != 1:
    st.session_state.currentStage = 1
    st.session_state.currentCase = 1
print(f"Case 1 script : {st.session_state.currentStage}")
currentCase = Case(currentCaseYml['caseNum'], currentCaseYml['caseDesc'],
                   currentCaseYml['maxStage'], currentCaseYml['questions'])
currentPage = CasePage(currentCase)
