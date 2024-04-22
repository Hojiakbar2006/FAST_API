from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = "f497bfa016043c381f35e29348726593a5edbea47028458407904a133dadeec526ef079ae9884543cfa4cadfecbb543fc3d7b922387683d9099bea9a066426dc"
ALGORITHM = "HS256"
TOKEN_EXPIRE_TIME = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')


def get_password_hash(password: str):
    return pwd_context.hash(password)


def create_access_token(data: dict, expire_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow()+timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt
