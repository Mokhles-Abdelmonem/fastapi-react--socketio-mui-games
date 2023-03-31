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
        players = await get_connected_players()
        await sio_server.emit('setPlayers', players)
        users_collection.update_one({"username" : username}, {"$set" : {"connected":True}})


@sio_server.event
async def disconnect(sid):
    user = await users_collection.find_one({"sid":sid})
    if user:
        users_collection.update_one({"sid":sid}, {"$set" : {"connected":False}})
        players = await get_connected_players()
        await sio_server.emit('setPlayers', players)
        sio_server.start_background_task(countdown_disconnected_user, user )



@sio_server.event
async def add_user(sid, username):
    player_obj = {
        "sid" : sid,
        "connected" : True,
        "in_room" : False,
        "room_number" : None,
        "player_won" : False,
        "player_lost" : False,
        "player_draw" : False,
        "side" : '',
        "status" : ''
    }
    users_collection.update_one({"username" : username}, {"$set" : player_obj})
    players_list = await get_connected_players()
    sio_server.enter_room(sid, "general_room")
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
    players = await get_connected_players()
    return players



@sio_server.event
async def player_logged_out(sid, username):
    player_obj = {
        "connected" : False,
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
    players = await get_connected_players()
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

@sio_server.event
async def check_player(sid, username):
    user = await users_collection.find_one({"username": username})
    if not user:
        players = await get_connected_players()
        await sio_server.emit('setPlayers', players)
        return False
    return True

@sio_server.event
async def get_rules(sid):
    rules = await retrieve_rules()
    return rules


@sio_server.event
async def game_request(sid,  username_x, username_o, role, game_type):
    context = {
        "username_x":username_x,
        "username_o":username_o,
        "role":role,
        "game_type":game_type
        }
    player = await users_collection.find_one({"username":username_o})
    await sio_server.emit('gameRequest', context, to=player["sid"])

@sio_server.event
async def decline_request(sid, username):
    player = await users_collection.find_one({"username":username})
    await sio_server.emit('requestDeclined', to=player["sid"])

@sio_server.event
async def cancel_request(sid,  username):
    player = await users_collection.find_one({"username":username})
    await sio_server.emit('requestCanceled', to=player["sid"])






@sio_server.event
async def join_room(sid, playerx, playero, game_type ,rule):
    room_number = "1"
    rooms = rooms_collection.find(sort=[( '_id', -1 )]).limit(1)
    rooms = await rooms.to_list(None)
    if rooms:
        last_room = rooms[0]
        last_room_number = last_room.get('room_number')
        room_number = str(int(last_room_number)+1) 


    player_x = await users_collection.find_one({"username":playerx})
    player_o = await users_collection.find_one({"username":playerx})
    sio_server.enter_room(player_x['sid'], room_number)
    sio_server.enter_room(player_o['sid'], room_number)

    sio_server.leave_room(player_x['sid'], 'general_room')
    sio_server.leave_room(player_o['sid'], 'general_room')
    player_update = {
        "player_won":False,
        "player_lost":False,
        "player_draw":False,
        "in_room":True,
        "room_number":room_number,
    }

    users_collection.update_one({"username" : playerx}, {"$set" : player_update})
    users_collection.update_one({"username" : playero}, {"$set" : player_update})

    timer_switch = {
        "x_time":15,
        "o_time":15,
        "x_turn":True,
        "player_won": False,
    }
    room = {
        "room_number":room_number,
        "player_x": playerx,
        "player_o": playero,
        "winner": None,
        "draw": False,
        "msgs": [],
        "timer_switch":timer_switch,
        "rule": rule,
        "game_type": game_type,
        "history": [None for i in range(9)],
        "rps_game": {},
        }

    rooms_collection.insert_one(room)
    players = await get_connected_players()
    await sio_server.emit('setPlayers', players)
    if game_type == 0:
        game_type_str = "Tic Tac Toe"
        sio_server.start_background_task(countdown_x, playerx, room_number, playero)
    elif game_type == 1:
        game_type_str = "Rock Paper Scissor"
        sio_server.start_background_task(start_rock_paper_scissor_game , playerx, room_number, playero )
    await sio_server.emit('cofirmAccepted', game_type_str,  to=player_x['sid'])
    await sio_server.emit('pushToRoom', to=room_number)
    print("join_room  >>>>>>>>> all pass successfully")


    