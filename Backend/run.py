from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import EmailStr, Field, BaseModel
from Backend.Backend_App.model import User
from Backend.Backend_App.model import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from Backend.config import Config
from Backend.helper import (
    generate_password_hash,
    is_password_valid,
    create_access_token,
    get_current_user,
)

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


class RegisterUser(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=8)
    confirm_password: str = Field(min_length=8)


class Login(BaseModel):
    email: EmailStr
    password: str


@app.post("/v1/AddUser")
async def registerUser(register: RegisterUser):
    """Create New User"""
    try:
        if register.password == register.confirm_password:
            add_user = User(
                username=register.username,
                email=register.email,
                password=generate_password_hash(register.password),
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
async def login(LoginUser: Login):
    """Login Account"""

    user = session.query(User).filter_by(Email=LoginUser.email).first()

    if not user or not is_password_valid(LoginUser.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="إيميل أو كلمة مرور خاطئة",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.Email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "Message": "Login Successful",
    }


@app.get("/v1/dashboard")
async def get_dashboard_data(current_user: str = Depends(get_current_user)):
    return {
        "Status": "Success",
        "Message": f"مرحباً بك في لوحة التحكم السرية يا {current_user}",
        "SecretData": "بيانات الجيم والمبيعات المشفرة هنا 🏋️‍♂️💰",
    }
