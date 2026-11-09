from functools import lru_cache
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    aws_region: str = 'ap-south-1'
    aws_access_key_id: str = ''    
    aws_secret_access_key: str = ''
    s3_bucket: str = ''
    database_url: str = ''  # Render PostgreSQL External Database URL
    bedrock_embed_model: str = 'amazon.titan-embed-text-v2:0'
    bedrock_chat_model: str = 'amazon.nova-lite-v1:0'
    embed_dim: int = 1024
    max_upload_bytes: int = 10485760
    pinecone_api_key: str = ''
    pinecone_index_name: str = 'nexora-enterprise-ai-index'
    pinecone_cloud: str = 'aws'
    pinecone_region: str = 'ap-south-1'
    pinecone_ready_timeout: int = 180
    min_relevance: float = 0.25
    hitl_enabled: bool = True
    memory_turns: int = 6

    @field_validator('hitl_enabled', mode='before')
    @classmethod
    def clean_bool(cls, v):
        if isinstance(v, str):
            v = v.strip().lower()
            if v in ('true', '1', 't', 'yes'):
                return True
            if v in ('false', '0', 'f', 'no'):
                return False
        return v

    @field_validator('*', mode='before')
    @classmethod
    def clean_strings(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v


@lru_cache
def settings() -> Settings:
    return Settings()
