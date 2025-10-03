# from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

# Table structure in DB
class user(SQLModel, table=True):
    id: Optional[int] =  Field(default_factory=None,primary_key=True)
    email: str=Field(nullable=False)
    username: str = Field(unique=True,nullable=False)
    hashPwd:str = Field(nullable=False)
    first_name:str= Field(nullable=False)
    middle_name: Optional[str] = Field(default_factory=None)
    last_name:str=Field(nullable=False)
    gender:Optional[str] = Field(default_factory=None) 
    # dob : datetime 
    
class User_Display(SQLModel):
    id:int 
    email: str
    username:str
    first_name:str
    middle_name: Optional[str]
    last_name:str
    gender:str
    # dob : datetime