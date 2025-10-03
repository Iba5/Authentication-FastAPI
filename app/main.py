from fastapi import FastAPI,Depends
from database.DbConn import *
from models.schemas import UserLogIn,UserSignUp
from auth.token import create_token
from auth.hashing import CreateHashedPwd
from contextlib import asynccontextmanager
from controller.endpoints import router as paths
from repository.dbcomm import info
# from fastapi.security import OAuth2PasswordRequestForm
from auth.authfoms import OAuth2PasswordRequestFormNoGrant

@asynccontextmanager
async def life_span(app:FastAPI):
    print("Starting Db")
    #logic for the db
    create_db()
    yield
    #close db as soon as the app stop
    engine.dispose()
    print("db closed")

apk=FastAPI(lifespan=life_span, title="Authenticator",description="Here we are going to filter all the user")
apk.include_router(paths)

#login info which verifies if the password provided matches that of the provided
@apk.post("/login")
async def login(
    form_data: OAuth2PasswordRequestFormNoGrant = Depends(),
    db: Session = Depends(get_db),
):
    user = UserLogIn(email=form_data.username, password=form_data.password)
    token = create_token(user, db)
    return {"access_token": token, "token_type": "bearer"}

@apk.post("/SignIn")
async def SignIn(user:UserSignUp,db:Session=Depends(get_db)):
    repo=info(db)
    user.password=CreateHashedPwd(user.password)
    # return user.password
    data=repo.Create(user)
    return data
