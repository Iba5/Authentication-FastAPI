from pydantic_settings import BaseSettings,SettingsConfigDict

#Importing the connection path of the db
class Settings(BaseSettings):
    database_url:str
    secret_key:str
    algorithm:str
    token_duration:int

    model_config = SettingsConfigDict(
        env_file= ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

#creating the bridge btwn sensitive inf and python
Config=Settings() #type: ignore

