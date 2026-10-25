from pytdantic import BaseSettings, Field


load_dotenv()

class Settings:
    api_key: str = Field(..., env="OPENAI_API_KEY")


    # Embedding Model
    embwedding_model: str = "text-embedding-ada-002",


settings = Settings()