from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Setttings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    #aws

    #pinecone

    #database
    database_url:str = ''
    supabase_url:str = ''
    supabase_key:str = ''

    #langsmith


@lru_cache
def settings() -> Setttings:
    return Setttings()