from sqlmodel import create_engine,Session,SQLModel
from config import Config
#creating Engine
engine = create_engine(Config.database_url,echo=True)

#Creating the db it self
def create_db():
    SQLModel.metadata.create_all(engine)
#Create Session responsible for operations done on DB
def get_db():
    with Session(autocommit=False, autoflush=False, bind=engine) as session:
        yield session
