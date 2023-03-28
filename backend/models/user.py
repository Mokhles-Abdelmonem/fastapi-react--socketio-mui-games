from pydantic import BaseModel, Field
from typing import Union

class RegisterJson(BaseModel):
    """
    """
    username: str
    email: Union[str, None] = None
    password: str


class LoginJson(BaseModel):
    """
    """
    username: str
    password: str

class AccessToken(BaseModel):
    access_token: str

class Token(AccessToken):
    refresh_token: str

class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    is_admin: Union[bool, None] = False
    disabled: Union[bool, None] = None
    joined: Union[bool, None] = None
    in_room: Union[bool, None] = None
    room_number: Union[str, None] = None
    sid: Union[str, None] = None
    side: Union[str, None] = None
    status: Union[str, None] = None
    level: Union[int, None] = None
    win_number: Union[int, None] = None
    player_won: Union[bool, None] = None
    player_lost: Union[bool, None] = None
    player_draw: Union[bool, None] = None
    connected: Union[bool, None] = None

class UserInDB(User):
    hashed_password: str

class Settings(BaseModel):
    authjwt_secret_key: str = "secret"


class UpdatedUserJson(BaseModel):
    """
    """
    level: int  | None = None
    disabled: bool | None = None
