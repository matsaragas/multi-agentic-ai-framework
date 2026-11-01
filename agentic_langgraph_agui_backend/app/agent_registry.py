from llm import ChatLLM, OpenAIEmbedding
from pydantic import BaseModel, Field



import structlog

loggert = structlog.get_logger()

class AgentRegistry:
    