from sqlmodel import create_engine,Session,SQLModel
from pydantic_settings import BaseSettings,SettingsConfigDict

#Importing the connection path of the db
class Settings(BaseSettings):
    database_url:str

    model_config = SettingsConfigDict(
        env_file= ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

#creating the bridge btwn DB and python
Config=Settings() #type: ignore

#creating Engine
engine = create_engine(Config.database_url,echo=True)

#Creating the db it self
def create_db():
    SQLModel.metadata.create_all(engine)
#Create Session responsible for operations done on DB
def get_db():
    with Session(autocommit=False, autoflush=False, bind=engine) as session:
        yield session
