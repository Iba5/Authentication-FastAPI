from pydantic_settings import BaseSettings,SettingsConfigDict
from decouple import config as con
#Importing the connection path of the db
class Settings(BaseSettings):
    database_url:str=con("database_url")
    secret_key: str = con("secret_key")
    algorithm: str=con("algorithm")
    token_duration:int= con("token_duration",cast=int,default=30)

    model_config = SettingsConfigDict(
        env_file= ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

#creating the bridge btwn sensitive inf and python
Config=Settings()

