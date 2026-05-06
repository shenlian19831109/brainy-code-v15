import os
from typing import Optional, Literal
from pydantic import BaseModel

class LLMConfig(BaseModel):
    provider: Literal["openai", "ollama", "huggingface_inference"] = "ollama"
    model_name: str = "codestral"
    api_key: Optional[str] = None
    base_url: Optional[str] = None

class EmbeddingConfig(BaseModel):
    provider: Literal["openai", "jina"] = "openai"
    model_name: str = "text-embedding-3-small"
    api_key: Optional[str] = None
    base_url: Optional[str] = None

class Config(BaseModel):
    llm: LLMConfig = LLMConfig()
    embedding: EmbeddingConfig = EmbeddingConfig()
    project_root: str = "."

    @classmethod
    def from_env(cls):
        return cls(
            llm=LLMConfig(
                provider=os.getenv("LLM_PROVIDER", "ollama"),
                model_name=os.getenv("LLM_MODEL", "codestral"),
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("LLM_BASE_URL")
            ),
            embedding=EmbeddingConfig(
                provider=os.getenv("EMBED_PROVIDER", "openai"),
                model_name=os.getenv("EMBED_MODEL", "text-embedding-3-small"),
                api_key=os.getenv("OPENAI_API_KEY") or os.getenv("JINA_API_KEY"),
                base_url=os.getenv("EMBED_BASE_URL")
            ),
            project_root=os.getenv("PROJECT_ROOT", ".")
        )