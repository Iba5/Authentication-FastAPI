from typing import Optional
from fastapi import Depends,HTTPException
import jwt 
from datetime import datetime,timedelta,timezone
from sqlmodel import Session
from config import Config
from models.schemas import UserLogIn
from database.DbConn import get_db
from auth.hashing import VerifyHashedPwd

#important things for encoding and decoding
algo = Config.algorithm
time_exp=Config.token_duration
key = Config.secret_key

# create a user_token
def create_token(User:UserLogIn,db:Session=Depends(get_db))->str:
    data=UserLogIn(**User.model_dump())
    if not VerifyHashedPwd(data.email,data.password,db):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    expire=datetime.now(timezone.utc)+timedelta(minutes=time_exp)
    payload:dict[str,int|str]={ 
                "sub":data.email,
                "iat":int(datetime.now(timezone.utc).timestamp()),
                "exp":int(expire.timestamp())
            }
    token=jwt.encode(payload,key,algorithm=algo)
    return token

# verify a user_token
def verify_token(token:str)->str:
    try:
        payload=jwt.decode(token,key,algorithms=[algo])
        sub: Optional[str] = payload.get("sub")
        if sub is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return sub
    except:
        raise HTTPException(status_code=401, detail="Invalid or expired token")