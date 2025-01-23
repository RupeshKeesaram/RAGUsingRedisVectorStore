from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Settings class to load and manage the application configuration from environment variables.

    This class uses Pydantic's `BaseSettings` to load settings from environment variables and a .env file.

    Attributes:
        REDIS_HOST (str): The host address for the Redis instance.
        REDIS_PORT (int): The port number for Redis.
        REDIS_DB (int): The Redis database index to use.
        REDIS_PASSWORD (Optional[str]): The password for connecting to Redis (if applicable).
        VECTOR_DIM (int): The dimension of the vector used for search, typically set to the OpenAI embedding dimension.
        TOP_K (int): The number of similar documents to return from the vector search.
        OPENAI_API_KEY (str): The API key used to authenticate with OpenAI.

    Config:
        env_file (str): The path to the `.env` file containing the environment variables.
    """

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None

    VECTOR_DIM: int = 1536
    TOP_K: int = 5

    OPENAI_API_KEY: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
