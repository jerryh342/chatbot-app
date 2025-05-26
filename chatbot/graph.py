import os
import time
from typing_extensions import List

import streamlit as st
from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langgraph.graph import END, StateGraph, MessagesState
from langgraph.graph.state import CompiledStateGraph
from langchain_core.documents import Document
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool
from langchain_core.prompts.chat import ChatPromptTemplate
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.rate_limiters import InMemoryRateLimiter
from .embedding import MistralAIEmbeddingsWithPause

rate_limiter = InMemoryRateLimiter(
    requests_per_second=1,  # Can only make a request once every 1 second
    check_every_n_seconds=0.5,  # Wake up every 500 ms to check whether allowed to make a request,
    max_bucket_size=10,  # Controls the maximum burst size.
)

model = ChatMistralAI(model="ministral-8b-latest",
                      api_key=st.secrets["MISTRAL_API_KEY"], rate_limiter=rate_limiter, temperature=0.63)
pc = Pinecone(api_key=st.secrets["PINECONE_API_KEY"])
lnt_index = pc.Index(name="diircb-lntguides")
embed = MistralAIEmbeddingsWithPause(api_key=st.secrets["MISTRAL_EMBED_API_KEY"])
vector_store = PineconeVectorStore(embedding=embed, index=lnt_index)


def query_or_respond(state: MessagesState):
    """Generate tool call for retrieval or respond."""
    llm_with_tools = model.bind_tools([retrieve])
    response = llm_with_tools.invoke(state["messages"])
    # MessagesState appends messages to state instead of overwriting
    return {"messages": [response]}


@tool(response_format="content_and_artifact")
def retrieve(query: str):
    """Retrieve information related to a query. https://python.langchain.com/docs/how_to/qa_chat_history_how_to/ """
    time.sleep(1.0)
    retrieved_docs = vector_store.similarity_search(query, k=3)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\n" f"Content: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs


# Step 3: Generate a response using the retrieved content.
def generate(state: MessagesState):
    """Generate answer."""
    # Get generated ToolMessages
    recent_tool_messages = []
    for message in reversed(state["messages"]):
        if message.type == "tool":
            recent_tool_messages.append(message)
        else:
            break
    tool_messages = recent_tool_messages[::-1]

    # Format into prompt
    docs_content = "\n\n".join(doc.content for doc in tool_messages)
    system_message_content = (
        "Use the following pieces of retrieved context only to answer "
        "the question. If you don't know the answer or the answer cannot be inferred from the context, say that you don't know."
        "\n\n"
        "CONTEXT:"
        f"{docs_content}"
    )
    conversation_messages = [
        message
        for message in state["messages"]
        if message.type in ("human", "system")
        or (message.type == "ai" and not message.tool_calls)
    ]
    prompt = [SystemMessage(system_message_content)] + conversation_messages

    # Run
    response = model.invoke(prompt)
    return {"messages": [response]}


def build_graph() -> CompiledStateGraph:
    tools = ToolNode([retrieve])
    graph_builder = StateGraph(MessagesState)

    graph_builder.add_node(query_or_respond)

    graph_builder.add_node(tools)
    graph_builder.add_node(generate)

    graph_builder.set_entry_point("query_or_respond")
    graph_builder.add_conditional_edges(
        "query_or_respond",
        tools_condition,
        {END: END, "tools": "tools"},
    )
    graph_builder.add_edge("tools", "generate")
    graph_builder.add_edge("generate", END)

    memory = MemorySaver()

    graph = graph_builder.compile(checkpointer=memory)
    return graph
