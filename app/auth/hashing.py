from passlib.context import CryptContext
from sqlmodel import Session,select
from models.table import user
from fastapi import Depends
from database.DbConn import get_db

pwd_hash=CryptContext(schemes=["bcrypt"],depracated="auto")
#creating a hashed password
def CreateHashedPwd(plain_pwd:str)->str:
    hashed_pwd=pwd_hash.hash(plain_pwd)
    return hashed_pwd

#verifying a hashed password
def VerifyHashedPwd(email:str,plain_pwd:str, db:Session= Depends(get_db))->bool:
    data=db.exec(select(user).where(user.email==email)).first()
    if data:
        return pwd_hash.verify(plain_pwd,data.hashPwd)
    return False


