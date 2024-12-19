import time
import logging
from typing import List

from langchain_mistralai import MistralAIEmbeddings
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
