from fastapi import Depends, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from fastapi import Depends, HTTPException, status
from models.user import RegisterJson, LoginJson
from fastapi_jwt_auth import AuthJWT
from utils.crud import * 
from models.user import Token, UserInDB, AccessToken
from pydantic import BaseModel




auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    access_expires: int = timedelta(minutes=300)
    refresh_expires: int = timedelta(days=30)

@AuthJWT.load_config
def get_config():
    return Settings()


@auth_router.post("/token/", response_model=Token)
async def login_for_access_token(json_data: LoginJson, Authorize: AuthJWT = Depends()):
    user = await authenticate_user(json_data.username, json_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user == "disabled":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="this account (Disabled) by admin",
            headers={"WWW-Authenticate": "Bearer"},
        )
    expires = timedelta(days=1)
    access_token = Authorize.create_access_token(subject=user['username'], expires_time=expires)
    refresh_token = Authorize.create_refresh_token(subject=user['username'])
    return {"access_token": access_token, "refresh_token": refresh_token}





@auth_router.post('/refresh/')
def refresh(Authorize: AuthJWT = Depends()):
    """
    """
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}


@auth_router.post('/verify/')
def verify( AccessToken: AccessToken, Authorize: AuthJWT = Depends()):
    user = Authorize._verified_token(AccessToken.access_token)
    return user

@auth_router.post("/register/", response_model=UserInDB, status_code=201)
async def user_register(json_data: RegisterJson):

    user_exist = await users_collection.find_one({"username": json_data.username})
    if user_exist:
        return JSONResponse(
        status_code=409,
        content={"username": f"username already exist"},
    )

    if not email_valid(json_data.email):
        return JSONResponse(
        status_code=501,
        content={"email": "Invalid email address"},
    )
    if not password_valid(json_data.password):
        return JSONResponse(
        status_code=400,
        content={"password": "Invalid password address enter at least 8 characters contain at least 1 number ,1 letter uppercase , 1 letter lowercase, 1 special character"},
    )

    user_valid = await validate_user(json_data.username, json_data.email,json_data.password)
    user = await users_collection.insert_one(user_valid)
    new_user = await users_collection.find_one({"_id": user.inserted_id})

    return new_user