import os
import time
import requests
import json
import streamlit as st
from sseclient import SSEClient


def getAuthToken() -> str:
    API_KEY = st.secrets['CUSTOMGPT_API_KEY']
    return f"Bearer {API_KEY}"


def getNewConversationID() -> str:
    projectID = os.getenv("CUSTOMGPT_PRJ_ID")
    authToken = getAuthToken()
    url = f"https://app.customgpt.ai/api/v1/projects/{projectID}/conversations"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": authToken
    }
    data = {
        "name": "test-convo"
    }
    response = requests.post(url, json=data, headers=headers)
    responseObj = json.loads(response.text)
    print(responseObj)
    return str(responseObj['data']['id'])


def updateConversation(prompt: str):
    projectID = st.secrets['CUSTOMGPT_PRJ_ID']
    sessionID = st.session_state.sessionID
    authToken = getAuthToken()
    url = f"https://app.customgpt.ai/api/v1/projects/{projectID}/conversations/{sessionID}/messages?stream=true"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": authToken
    }
    data = {
        "prompt": prompt
    }
    response = requests.post(url, json=data, headers=headers, stream=True)
    client = SSEClient(response)
    for event in client.events():
        eventJSON = json.loads(event.data)
        if eventJSON['status'] == "progress":
            yield eventJSON['message']
            time.sleep(0.05)
