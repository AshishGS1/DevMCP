from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str | None = None
    collection: str = "Devs"
    model_name: str = "all-MiniLM-L6-v2"
    dims: int = 384

    host: str = "127.0.0.1"
    port: int = 8002

    page_size: int = 15
    top_k: int = 3
    score_threshold: float = 0.3

setting = Settings()