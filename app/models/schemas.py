from typing import Optional
from pydantic import BaseModel
from datetime import datetime
# user-info
class User(BaseModel):
    id:int 
    first_name:str
    middle_name: Optional[str]
    last_name:str
    gender:str
    dob : datetime
    email: str

# user-log-in
class UserLogIn(BaseModel):
    email:str
    password:str

# user-sign-up
class UserSignUp(BaseModel):
    first_name:str
    middle_name: Optional[str]
    last_name:str
    gender:str
    dob : datetime
    email: str