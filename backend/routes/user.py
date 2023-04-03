from fastapi import Depends, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from fastapi import Depends, HTTPException, status
from models.user import RegisterJson, LoginJson, UpdatedUserJson
from fastapi_jwt_auth import AuthJWT
from utils.crud import * 
from sockets.server import sio_server 
from sockets.games import stop_time_back, player_left_in_game, leave_room
from models.user import Token, UserInDB
from pydantic import BaseModel




users_router = APIRouter(
    prefix="/users",
    tags=["User"]
)

@users_router.get("/")
async def read_users(current_user: User = Depends(get_current_active_user)):
    users = await retrieve_users()
    if users :
        return ResponseUsersList(users, current_user)
    
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"notfound": "Empty list returned"},
        )

@users_router.get("/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@users_router.get("/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user['username']}]


@users_router.post("/admin_update_users/{username}/")
async def admin_update_users(username , updated_user: UpdatedUserJson, current_user: User = Depends(get_current_active_user)):
    
    if not current_user['is_admin']:
        return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"error": "UNAUTHORIZED to update users"},
    )
    user_update = {
        "level":updated_user.level,
        "disabled":updated_user.disabled
        }
    if updated_user.disabled:
        user = await users_collection.find_one({"username" : username})
        if not user:
            return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "no users found with this username"},
        )
        sid = user.get('sid')
        if sid:
            in_room = user.get('in_room')
            if in_room:
                room = await rooms_collection.find_one({"room_number" : user["room_number"]})
                opponent_name = room["player_x"] if room["player_x"] != username else room["player_o"]
                await player_left_in_game(sid, opponent_name)
                await leave_room(sid, username, opponent_name)
            await sio_server.emit('logeUserOut', to=sid)
        user_update = {
            "joined" : True,
            "in_room" : False,
            "room_number" : None,
            "player_won" : False,
            "player_lost" : False,
            "player_draw" : False,
            "side" : '',
            "status" : '',
            "level":updated_user.level,
            "disabled":updated_user.disabled
            }

    users_collection.update_one({"username" : username}, {"$set" : user_update})
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"success": "User successfully updated"},
    )


@users_router.delete("/admin_delete_users/{username}/")
async def admin_delete_users(username , current_user: User = Depends(get_current_active_user)):

    if not current_user['is_admin']:
        return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"error": "UNAUTHORIZED to delete users"},
    )
    user = await users_collection.find_one({"username" : username})
    if not user:
        return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": "no users found with this username"},
    )
    sid = user.get('sid')
    if sid:
        in_room = user.get('in_room')
        if in_room:
            room = await rooms_collection.find_one({"room_number" : user["room_number"]})
            opponent_name = room["player_x"] if room["player_x"] != username else room["player_o"]
            await player_left_in_game(sid, opponent_name)
            await leave_room(sid, username, opponent_name)
        await sio_server.emit('logeUserOut', to=sid)

    users_collection.delete_one({"username" : username})

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"success": "User deleted "},
    )
