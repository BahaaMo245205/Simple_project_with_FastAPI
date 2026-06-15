from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from pydantic import ValidationError
from dotenv import load_dotenv
from jose import jwt
import hashlib
import os

load_dotenv()
security_scheme = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_password_hash(password: str) -> str:
    sha256_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return sha256_hash


def is_password_valid(plain_password: str, hashed_password: str) -> bool:
    sha256_hash = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
    if sha256_hash == hashed_password:
        return True
    return None


def create_access_token(data: dict) -> dict:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    )
    to_encode.update({"exp": expire})

    encode_jwt = jwt.encode(
        to_encode, str(os.getenv("SECRET_KEY")), algorithm=str(os.getenv("ALGORITHM"))
    )
    return encode_jwt


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
) -> str:
    """
    الدالة دي بتشتغل كـ Dependency لفحص التوكن وتأكيده
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            str(os.getenv("SECRET_KEY")),
            algorithms=[str(os.getenv("ALGORITHM"))],
        )

        user_email: str = payload.get("sub")
        if user_email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="توكن غير صالح: البيانات ناقصة.",
            )

        return user_email

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="انتهت صلاحية التوكن، سجل دخول تاني يا بطل.",
        )
    except (jwt.InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="التوكن ده مضروب وغير صالح! 🚨",
        )
