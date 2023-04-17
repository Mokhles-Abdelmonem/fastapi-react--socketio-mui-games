
from typing import Union
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
import re
from schemas.user import ResponseModel, user_helper, ResponseUsersList
from fastapi_jwt_auth import AuthJWT
from config.db import users_collection, rule_collection, rooms_collection, msgs_collection
from models.user import User








SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30




pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(username: str):
    user = await users_collection.find_one({"username":username})
    return user


async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user :
        return False
    if user['disabled']:
        return "disabled"
    verifyed = verify_password(password, user["hashed_password"])
    if not verifyed:
        return False
    return user


def email_valid(s):
   pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
   if re.match(pat,s):
      return True
   return False



def password_valid(s):
   pat = "^.{3,}$"
   if re.match(pat,s):
      return True
   return False


async def validate_user(username: str, email: str, password: str):
    user = await get_user(username)
    if user:
        return False
    # if not verify_password(password, user.hashed_password):
    #     return False
    return {"username": username, "email": email, "hashed_password": get_password_hash(password), "disabled":False}




async def user_exist(username: str):
    user = await get_user(username)
    if user:
        return True
    return False



def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



async def get_current_user(Authorize: AuthJWT = Depends()):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user = await get_user(username=current_user)
    if user is None:
        raise credentials_exception
    return user



async def get_current_active_user(current_user: User = Depends(get_current_user)):
    # if current_user['disabled']:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def retrieve_users():
    users = []
    async for user in users_collection.find():
        users.append(user)
    return users

