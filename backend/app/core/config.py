from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    RAPIDAPI_KEY: str = ""
    RAPIDAPI_HOST: str = ""
    MONGO_DETAILS: str = "mongodb://localhost:27017"
    LLM_PROVIDER: str = "openai"
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
