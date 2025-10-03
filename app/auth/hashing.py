from passlib.hash import bcrypt
from sqlmodel import Session,select
from models.table import user
from fastapi import Depends
from database.DbConn import get_db

#creating a hashed password
def CreateHashedPwd(plain_pwd:str)->str:
    
    return bcrypt.hash(plain_pwd[:72])

#verifying a hashed password
def VerifyHashedPwd(email:str,plain_pwd:str, db:Session= Depends(get_db))->bool:
    data=db.exec(select(user).where(user.email==email)).first()
    if data:
        return bcrypt.verify(plain_pwd,data.hashPwd)
    return False


