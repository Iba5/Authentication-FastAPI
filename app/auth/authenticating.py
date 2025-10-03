from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException
from sqlmodel import Session
from database.DbConn import get_db
from auth.token import verify_token
from repository.dbcomm import info

auth=OAuth2PasswordBearer(tokenUrl="/login")

async def get_current_user(token:str=Depends(auth), db:Session=Depends(get_db)):
    email= verify_token(token)
    repo=info(db)
    user=repo.GetUser(email)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    return user