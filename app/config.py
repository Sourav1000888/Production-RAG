from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Setttings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    
    #models
    embedding_model='sentencetransformer'
    huggingface_api_key:str = ''
    embed_dim=384
    chat_model='gemma4:cloud'
    ollama_api_key:str = ''

    #pinecone
    pinecone_api_key = ''
    pinecone_cloud=''
    pinecone_region=''
    pinecone_ready_timeout=3.3
    pinecone_index_name='dot'

    #database
    database_url:str = ''
    supabase_url:str = ''
    supabase_key:str = ''

    #langsmith


@lru_cache
def settings() -> Setttings:
    return Setttings()