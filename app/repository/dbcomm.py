from typing import List,Optional,Union
from abc import ABC,abstractmethod
from sqlmodel import Session,select
from fastapi import Depends
from database.DbConn import get_db
from models.table import user
from models.table import User_Display
from models.schemas import UserSignUp, UserUpdate

class InterComm(ABC):
    @abstractmethod
    def GetUser(self,id:Union[int,str])->Optional[User_Display]:
        pass
    @abstractmethod
    def Getall(self)->List[User_Display]:
        pass
    @abstractmethod
    def Update(self, id:Union[int,str],update:UserUpdate)->Optional[User_Display]:
        pass
    @abstractmethod
    def Delete(self,id:Union[int,str])->Optional[User_Display]:
        pass
    @abstractmethod
    def Create(self,details:UserSignUp)->User_Display:
        pass

class info(InterComm):
    
    def __init__(self,db:Session=Depends(get_db)):
        self.db=db

    def get_by_id(self,id:Union[int,str]):
        if  isinstance(id,str):
            return self.db.exec(select(user).where(user.email==id)).first()
        return self.db.exec(select(user).where(user.id==id)).first()
    
    def GetUser(self,id:Union[int,str])->Optional[User_Display]:
        data= self.get_by_id(id)
        if not data:
            return None
        return User_Display.model_validate(data)
    
    def Getall(self)->List[User_Display]:
        statement=select(user)
        data=self.db.exec(statement).all()
        if not data:
            return []
        return [User_Display.model_validate(item) for item in data]
    
    def Update(self,id:Union[int,str],update:UserUpdate) -> User_Display | None:
        data= self.get_by_id(id)
        if data:
            update_data=update.model_dump()
            for field, value in update_data.items():
                setattr(data,field,value)
            self.db.commit()
            self.db.refresh(data)    
            return User_Display.model_validate(data)
        return None
    
    def Delete(self,id:Union[int,str])->User_Display|None:
        data=self.get_by_id(id)
        if not data:
            return None
        self.db.delete(data)
        self.db.commit()
        self.db.refresh(data)
        return User_Display.model_validate(data)
    
    def Create(self,details:UserSignUp):
        # return details.password       
        user_data=user(
            email=details.email,
            username=details.username,
            hashPwd=details.password,
            first_name=details.first_name,
            middle_name=details.middle_name or "",
            last_name=details.last_name,
            gender=details.gender or "")
        try:
            self.db.add(user_data)
            self.db.commit()
            self.db.refresh(user_data)
        except:
            self.db.rollback()
            raise
        return User_Display.model_validate(user_data)