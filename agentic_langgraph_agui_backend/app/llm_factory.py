import structlog
from pydantic import BaseModel
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from langchain_core.prompts import PromptTemplate
from config import settings
from langchain_openai import ChatOpenAI


logger = structlog.get_logger(__name__)

def load_prompt(prompt, context: dict):
    return PromptTemplate.from_template(prompt).format(**context)

class ChatLLM:

    def __init__(self, temperature: float = 0.01):
        self.client = self._create_client(temperature)

    def _create_client(self, temperature: float) -> OpenAI:
        common_params = {
            "api_key": settings.api_key,
            "model": settings.model,
        }
        return ChatOpenAI(
            model="gpt-4o",
            api_key=settings.api_key,
            temperature=0,
            max_tokens=None,
            max_retries=2,)

    async def query(
            self,
            system_prompt: str | tuple | None,
            user_prompt: str | tuple | None,
            response_format: type[BaseModel] | None = None,
    ):
        if isinstance(system_prompt, tuple):
            system_prompt = load_prompt(system_prompt[0], system_prompt[1])

        if isinstance(user_prompt, tuple):
            user_prompt = load_prompt(user_prompt[0], user_prompt[1])

        messages = [("system", system_prompt), ("human", user_prompt)]

        try:
            if not response_format:
                ai_msg = await self.client.ainvoke(messages)
            else:
                structured_llm = self.client.with_structured_output(response_format)
                ai_msg = await structured_llm.ainvoke(messages)

            token_usage = None
            if hasattr(ai_msg, 'usage_metadata') and ai_msg.usage_metadata:
                token_usage = {
                    "input_tokens": ai_msg.usage_metadata.get("input_tokens"),
                    "output_tokens": ai_msg.usage_metadata.get("output_tokens"),
                    "total_tokens": ai_msg.usage_metadata.get("total_tokens"),
                }
            elif hasattr(ai_msg, 'response_metadata') and ai_msg.response_metadata:
                usage = ai_msg.response_metadata.get("token_usage", {})
                if usage:
                    token_usage = {
                        "input_tokens": usage.get("prompt_tokens"),
                        "output_tokens": usage.get("completion_tokens"),
                        "total_tokens": usage.get("total_tokens"),
                    }

            return ai_msg

        except Exception as e:
            logger.error("Error during LLM query", error=str(e))
            raise


class EmbeddingLLM:

    def __init__(self):
        self.client = self._create_client()

    def _create_client(self) -> OpenAIEmbedding:
        
        return OpenAIEmbedding(
            max_retries=50,
            chunk_size=50,
            model=settings.embedding_model,
            api_key=settings.api_key
        )




def llm():
    return ChatLLM().client