from repository.dbcomm import info
from database.DbConn import get_db
from fastapi import APIRouter,Depends
from auth.hashing import *
from auth.token import *
from models.schemas import *
from auth.authenticating import get_current_user
from typing import Union
from service.serviceside import Service

router = APIRouter(prefix="/user",tags=["user"],dependencies=[Depends(get_current_user)])

#create a user
@router.post("/AddUser")
async def AddUser(user:UserSignUp,db:Session=Depends(get_db)):
    user.password=CreateHashedPwd(user.password)
    repo= info(db)
    serv=Service(repo)    
    return serv.Add_New_User(user)

#update a user
@router.patch("/UpdateUserDetails/id")
async def UpdateUser(id:Union[int,str],user:UserUpdate,db:Session=Depends(get_db)):
    repo= info(db)
    serv=Service(repo)    
    return serv.Update_User(id,user)

#delete a user
@router.delete("/DeleteUser/id")
async def DeleteUser(id:Union[int,str],db:Session=Depends(get_db)):
    repo= info(db)
    serv=Service(repo)

    return serv.Remove_User(id)

#display a user
@router.get("Display/id")
async def DisplayUser(id:Union[int,str],db:Session=Depends(get_db)):
    repo= info(db)
    serv=Service(repo)
    return serv.Display_User(id)

#display all users
@router.get("/Display")
async def DisplayAll(db:Session=Depends(get_db)):
    repo= info(db)
    serv=Service(repo)
    return serv.Display_All()


