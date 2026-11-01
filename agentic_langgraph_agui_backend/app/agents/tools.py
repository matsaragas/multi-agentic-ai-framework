import structlog

logger = structlog.get_logger()

class AgentTools:
    def __init__(self, agent_registry=None):
        self.agent_registry = agent_registry