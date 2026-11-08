from llm import ChatLLM, OpenAIEmbedding
from pydantic import BaseModel, Field



import structlog

loggert = structlog.get_logger()

class AgentRegistry:
    def __init__(
        self,
        client=None,
        embedding_model=None,
        resolver: A2ACardResolver = None,
        llm=None
    ):
        self.client = client
        self.embedding_model = embedding_model or EmbeddingLLM().client
        self.resolver = resolver
        self.llm = llm or ChatLLM()


