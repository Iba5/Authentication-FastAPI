from typing import Union
from repository.dbcomm import info
# from database.DbConn import get_db
from fastapi import HTTPException
from models import schemas as sh
 

#Class which consists of all the business logic
class Service:
    #Creating a new user
    def __init__(self,repo:info):
        self.repo=repo

    def Add_New_User(self,signup:sh.UserSignUp):
        data=self.repo.Create(signup)
        return data
    
    #Making changes on existing user
    def Update_User(self,id:Union[int,str],update:sh.UserUpdate):
        data=self.repo.Update(update.id,update)
        if not data:
            raise HTTPException(status_code=401, detail="The user doesn't exist in our db")
        return data
    
    #removing user from the db
    def Remove_User(self,id:Union[int,str]):
        data=self.repo.Delete(id)
        if not data:
            raise HTTPException(status_code=404, detail="User does not exist")
        return data
        
    #displaying info about a user
    def Display_User(self,id:Union[int,str]):
        data=self.repo.GetUser(id)
        if not data:
            raise HTTPException(status_code=404, detail="Invalid information provided")
        return data
    
    #displaying all the user and their info
    def Display_All(self):
        return self.repo.Getall()
