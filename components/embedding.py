import os
import time
import logging

import streamlit as st

from langchain_core.documents import Document
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import MarkdownTextSplitter, CharacterTextSplitter
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
from typing import List

logger = logging.getLogger(__name__)


class MistralAIEmbeddingsWithPause(MistralAIEmbeddings):
    def __init__(self, api_key: str):
        super().__init__(api_key=api_key)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of document texts.

        Args:
            texts: The list of texts to embed.

        Returns:
            List of embeddings, one for each text.
        """
        try:
            batch_responses = []
            for batch in self._get_batches(texts):
                batch_responses.append(
                    self.client.post(
                        url="/embeddings",
                        json=dict(
                            model=self.model,
                            input=batch,
                        ),
                    )
                )
                time.sleep(1.6)
            batch_responses = tuple(batch_responses)
            return [
                list(map(float, embedding_obj["embedding"]))
                for response in batch_responses
                for embedding_obj in response.json()["data"]
            ]
        except Exception as e:
            logger.error(f"An error occurred with MistralAI: {e}")
            raise


class EmbedPage():
    def __init__(self, index_name: str = "diircb-lntguides"):
        self.embed = MistralAIEmbeddingsWithPause(st.secrets['MISTRAL_EMBED_API_KEY'])
        self.pc = Pinecone(api_key=st.secrets['PINECONE_API_KEY'])
        self.index = self.pc.Index(name=index_name)
        self.vector_store = PineconeVectorStore(embedding=self.embed, index=self.index)
        self.mdSplitter = MarkdownTextSplitter()
        self.charSplitter = CharacterTextSplitter(
            separator="\n\n",
            chunk_size=1024,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False,
        )

    def load_page(self) -> None:
        """
        Loads the page
        """
        st.title("Embed new documents")
        self.uploaded_files = st.file_uploader("Upload .txt files", type='txt', accept_multiple_files=True)
        st.button("Embed documents", on_click=self.embed_docs)

    def get_documents(self) -> list[Document]:
        docs_list = []
        for file in self.uploaded_files:
            string = file.read().decode("utf-8")
            meta = {
                "source": file.name,
            }
            doc = Document(page_content=string, metadata=meta)
            docs_list.append(doc)
            # st.write(string)
        return docs_list

    def embed_docs(self):
        doc_chunks = self.mdSplitter.split_documents(self.get_documents())
        chunks = self.charSplitter.split_documents(doc_chunks)
        print(len(chunks))
        doc_ids = self.vector_store.add_documents(chunks)
        if doc_ids:
            st.success(f"Successfully embedded {len(doc_ids)} chunks from {len(self.uploaded_files)} files")
        else:
            st.error(f"Embedding failed, please check console for details")
        return None


page = EmbedPage()
page.load_page()
