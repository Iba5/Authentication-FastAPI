from typing import Optional
from pydantic import BaseModel
# from datetime import datetime
# user-info
class UserUpdate(BaseModel):
    id:int
    first_name:Optional[str]
    middle_name: Optional[str]
    last_name:Optional[str]
    gender:Optional[str]
    # dob : Optional[datetime] 
    email: Optional[str]

# user-log-in
class UserLogIn(BaseModel):
    email:str
    password:str

# user-sign-up
class UserSignUp(BaseModel):
    email: str
    username:str
    password:str
    first_name:str
    middle_name: Optional[str]
    last_name:str
    gender:str
    password:str