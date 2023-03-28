from .utils import * 
from fastapi_jwt_auth import AuthJWT


def stop_time_back(room):
    pass

@sio_server.event
async def connect(sid, environ, auth):
    if auth:
        Authorize = AuthJWT()
        user_auth = Authorize._verified_token(auth)
        username = user_auth['sub']
        users_collection.update_one({"username" : username}, {"$set" : {"connected":True}})


@sio_server.event
async def disconnect(sid):
    user = await users_collection.find_one({"sid":sid})
    if user:
        users_collection.update_one({"username" : user["username"]}, {"$set" : {"connected":False}})
        sio_server.start_background_task(countdown_disconnected_user, user )



@sio_server.event
async def add_user(sid, username):
    print(f" ________________ add_user {username}   _____________________")
    player_obj = {
        "sid" : sid,
        "joined" : True,
        "in_room" : False,
        "room_number" : None,
        "player_won" : False,
        "player_lost" : False,
        "player_draw" : False,
        "side" : '',
        "status" : ''
    }
    users_collection.update_one({"username" : username}, {"$set" : player_obj})
    players_list = await get_joined_players()
    sio_server.enter_room(sid, "general_room")
    print(f" ________________  players_list {players_list}   _____________________")
    await sio_server.emit('playerJoined', {'username': username, "players":players_list} , to="general_room")



@sio_server.event
async def get_player(sid, username):
    player = await users_collection.find_one({"username" : username})
    return player_helper(player)


@sio_server.event
async def update_player_session(sid, username):
    users_collection.update_one({"username" : username}, {"$set" : {"sid": sid}})
    player = await users_collection.find_one({"username" : username})
    if player['in_room']:
        sio_server.enter_room(sid, player['room_number'])
    else:
        sio_server.enter_room(sid,"general_room")
    players = await get_joined_players()
    return players



@sio_server.event
async def player_logged_out(sid, username):
    player_obj = {
        "joined" : False,
        "in_room" : False,
        "room_number" : None,
        "player_won" : False,
        "player_lost" : False,
        "player_draw" : False,
        "win_number" : 0,
        "side" : '',
        "status" : ''
    }
    player = await users_collection.find_one({"username":username})
    room = player['room_number']
    sid = player['sid']
    sio_server.leave_room(sid, room)
    users_collection.update_one({"username":username}, {"$set" : player_obj})
    players = await get_joined_players()
    await sio_server.emit('setPlayers', players)




@sio_server.event
async def chat(sid, username, message):
    msgs_collection.insert_one(
        {
        'message': message,
        'username': username,
        'type': 'chat'
         }
    )
    messages = await get_chat_messages()
    await sio_server.emit('chat', messages, to='general_room')


@sio_server.event
async def get_messages(sid):
    messages = await get_chat_messages()
    return messages

