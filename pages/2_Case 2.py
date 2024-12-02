import yaml
import streamlit as st
from components.casePage import CasePage
from schema.schema import Case

with open('./data/cases/case2.yml', 'r') as file:
    currentCaseYml = yaml.safe_load(file)['case']
st.session_state.currentStage = 1

currentCase = Case(currentCaseYml['caseNum'], currentCaseYml['caseDesc'], currentCaseYml['questions'])
currentPage = CasePage(currentCase)
