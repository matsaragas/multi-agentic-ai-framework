import json
from typing import Literal
import structlog
from agent_registry import AgentRegistry

from langchain_core.runnables.config import RunnableConfig
from llm import ChatLLM

from shemas import AgentState, AgentTools


logger = structlog.get_logger()

class OrchestatorAgentGraph:
    def __init__(self, agent_registry: AgentRegistry = None, tools: AgentTools = None, llm: ChatLLM = None):
        self.agent_registry = agent_registry or AgentRegistry()
        self.tools = tools or AgentTools()
        self.llm = llm or ChatLLM()



    async def chatbot_node(
        self, state: AgentState, config: RunnableConfig
    ):
    """
    Chatbot node for the orchestration agent graph. 
    This node handles the interaction with the user and handles general queries.
    """

    async def context_manager_node(
        self, state: AgentState, config: RunnableConfig
    ):
        """
        Context manager node for the orchestration agent graph. 
        This node manages the context and state of the conversation.
        """