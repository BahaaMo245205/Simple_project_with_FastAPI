from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, status
from pydantic import EmailStr, Field,BaseModel
from Backend.Backend_App.model import User
from Backend.Backend_App.model import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from Backend.config import Config
import hashlib

engine = create_engine(Config.db)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def hash_password(password: str) -> str:
    sha256_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return sha256_hash


def verify_password(plain_password: str, hashed_password: str) -> bool:
    sha256_hash = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
    if sha256_hash == hashed_password:
        return True

    return None

class RegisterUser (BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=8)
    confirm_password: str = Field(min_length=8)

class Login (BaseModel):
    email:EmailStr
    password:str

@app.post("/v1/AddUser")
async def registerUser(
    register=RegisterUser
):
    """Create New User"""
    try:
        if register.password == register.confirm_password:
            add_user = User(
                username=register.username, email=register.email, password=hash_password(register.password)
            )
            if add_user:
                session.add(add_user)
                session.commit()
                {"Status": "Success", "Message": "User Added Successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong Passowrd !"
            )
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error : {e}"
        )


@app.post("/v1/login")
async def login(LoginUser=Login):
    """Login Account"""

    user = session.query(User).filter_by(Email=LoginUser.email).first()
    if user and verify_password(plain_password=LoginUser.password, hashed_password=user.password):
        return {"Status": "Success", "Message": f"Hello {user.UserName}"}

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Something Wrong enail or password .",
        )
