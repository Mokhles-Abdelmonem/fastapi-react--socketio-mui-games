from .utils import * 
from fastapi_jwt_auth import AuthJWT
from .chess import base_board

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
        if user['in_room']:
            sio_server.start_background_task(countdown_disconnected_user, user )



@sio_server.event
async def add_user(sid, username):
    player_obj = {
        "sid" : sid,
        "joined" : True,
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
    player.pop("_id")
    room_number = player.get("room_number")
    opponent_name = None
    if room_number:
        room = await rooms_collection.find_one({"room_number" : room_number})
        opponent_name = room["player_x"] if room["player_x"] != username else room["player_o"]
    if player['in_room']:
        sio_server.enter_room(sid, player['room_number'])
    else:
        sio_server.enter_room(sid,"general_room")
    players = await get_connected_players()
    return {"players_list":players, "player":player, "opponent_name":opponent_name}



@sio_server.event
async def player_logged_out(sid, username, opponent_name):
    player_update = {
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
    await users_collection.update_one({"username":username}, {"$set" : player_update})
    if opponent_name:
        await users_collection.update_one({"username":opponent_name}, {"$set" : player_update})
    opponent = await users_collection.find_one({"username":opponent_name})
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
async def game_request(sid,  username_x, username_o, rule, game_type):
    context = {
        "username_x":username_x,
        "username_o":username_o,
        "rule":rule,
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
    player_o = await users_collection.find_one({"username":playero})
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
    room = {
        "room_number":room_number,
        "player_x": playerx,
        "player_o": playero,
        "winner": None,
        "draw": False,
        "x_time":15,
        "o_time":15,
        "x_turn":True,
        "msgs": [],
        "rule": rule,
        "game_type": game_type,
        "history": [None for i in range(9)],
        "rps_game": {},
        "chess_board": base_board,
        "chess_moves": 0,
        "black_king_position":[0,4],
        "white_king_position":[7,4],
        "check":None,
        "forced_moves":[],
        "mate": False,
        "K_moved" : False,
        "k_moved" : False,
        "R_0_moved" : False,
        "r_0_moved" : False,
        "R_7_moved" : False,
        "r_7_moved" : False,
        "en_passant" :[],
        "en_passant_to" :[],
        }

    await rooms_collection.insert_one(room)
    players = await get_connected_players()
    await sio_server.emit('setPlayers', players)
    if game_type == 0:
        game_type_str = "Tic Tac Toe"
        sio_server.start_background_task(countdown_x, playerx, room_number, playero)
    elif game_type == 1:
        game_type_str = "Rock Paper Scissor"
        sio_server.start_background_task(start_rps_game , playerx, room_number, playero )
    elif game_type == 2:
        game_type_str = "Chess"
    await sio_server.emit('cofirmAccepted', game_type_str,  to=player_x['sid'])
    await sio_server.emit('pushToRoom', to=room_number)


@sio_server.event
async def chat_in_room(sid, username, message):
    message = {
        'sid': sid,
        'message': message,
        'username': username,
        'type': 'chat'
        }
    user = await users_collection.find_one({"username": username})
    room_number = user["room_number"]
    room = await rooms_collection.find_one({"room_number": room_number})
    msgs = room["msgs"]
    msgs.append(message)
    rooms_collection.update_one({"room_number": room_number}, {"$set" : {"msgs":msgs}})
    await sio_server.emit('chatInRoom', msgs, to=room_number)

@sio_server.event
async def get_chat_in_room(sid, username):
    user = await users_collection.find_one({"username": username})
    room = await rooms_collection.find_one({"room_number": user["room_number"]})
    return room["msgs"]


@sio_server.event
async def get_board(sid, username):
        user = await users_collection.find_one({"username": username})
        room = await rooms_collection.find_one({"room_number": user["room_number"]})
        return room["history"]


@sio_server.event
async def get_user_level(sid, username):
    player = await users_collection.find_one({"username": username})
    return player['level']



@sio_server.event
async def handle_click(sid, i, username):
    player = await users_collection.find_one({"username": username})
    room_number = player['room_number']
    room = await rooms_collection.find_one({"room_number": room_number})

    player_time = room["x_time"] if room["player_x"] == username else room["x_time"]
    room_history = room["history"]
    rule = room["rule"]
    rule_obj = await rule_collection.find_one({"winning_number": rule})
    winner = calculate_winner(room_history, rule_obj["rules"])
    player_turn = get_player_turn(room_history)
    player_won = room["winner"]
    if winner or room_history[i] or not player_time or room[player_turn] !=username or player_won :
        return
    opponent_name = room["player_o"] if room["player_x"] == username else room["player_x"]
    await switch_timer(player, opponent_name, player_turn)
    side = "X" if player_turn == "player_x" else "O"
    room_history[i] = side
    winner = calculate_winner(room_history, rule_obj["rules"])
    if winner == 'tie':
        await declare_draw(username, room_number, opponent_name)
    elif winner :
        opponent = await users_collection.find_one({"username": opponent_name})
        await declare_winner(player, opponent, room)


    rooms_collection.update_one({"room_number": room_number}, {"$set" : {"history":room_history}})
    await sio_server.emit('setBoard', room_history , to=room_number)

@sio_server.event
async def rematch_game(sid, room_number):
    player_update = {
        "player_won" : False,
        "player_lost" : False,
        "player_draw" : False
    }
    room_update = {
        "winner": None,
        "draw": False,
        "x_time":15,
        "o_time":15,
        "x_turn":True,
        "history": [None for i in range(9)],
        "rps_game": {},
        }
    room = await rooms_collection.find_one({"room_number": room_number})
    player_o = room["player_o"]
    player_x = room["player_x"]
    users_collection.update_one({"username" : player_x}, {"$set" : player_update})
    users_collection.update_one({"username" : player_o}, {"$set" : player_update})
    rooms_collection.update_one({"room_number": room_number}, {"$set" : room_update})
    if room["game_type"] == 0:
        sio_server.start_background_task(countdown_x, player_x, room_number, player_o)
    if room["game_type"] == 1:
        sio_server.start_background_task(start_rps_game, player_x, room_number, player_o)
    await sio_server.emit('rematchGame', to=room_number)


@sio_server.event
async def player_left_room(sid, opponent_name):
    opponent =  await users_collection.find_one({"username": opponent_name})
    await sio_server.emit('notePlayerLeft', to=opponent['sid'])
    players = await get_connected_players()
    await sio_server.emit('setPlayers', players)


@sio_server.event
async def leave_room(sid, username, opponent_name):
    player = await users_collection.find_one({"username": username})
    room = player['room_number']
    sid = player['sid']
    sio_server.enter_room(sid, 'general_room')
    sio_server.leave_room(sid, room)
    player_update = {
        "in_room" : False,
        "room_number" : None,
        "player_won" : False,
        "player_lost" : False,
        "player_draw" : False,
        "win_number" : 0,
        "side" : '',
    }
    await users_collection.update_one({"username" : username}, {"$set" : player_update})
    await users_collection.update_one({"username" : opponent_name}, {"$set" : player_update})
    players = await get_connected_players()
    await sio_server.emit('setPlayers', players)




@sio_server.event
async def player_left_in_game(sid, opponent_name):
    player = await users_collection.find_one({"username": opponent_name})
    room_number = player['room_number']
    room = await rooms_collection.find_one({"room_number": room_number})
    win_number = player.get('win_number')
    player_level = player.get('level')
    if not player_level:
        player['level'] = 1
    rule = room.get("rule")
    if win_number != None:
        if win_number >= 0: 
            player['win_number'] += 1
            if player['win_number'] % rule == 0 :
                player['level'] += 1
    else:
        player['win_number'] = 0
    player['player_won'] = True
    player.pop('_id')
    rooms_collection.update_one({"room_number": room_number}, {"$set" : {"winner":opponent_name}})
    users_collection.update_one({"username" : opponent_name}, {"$set" : player})
    await sio_server.emit('declareWinner', {'winner': opponent_name, 'roomNumber':room_number})
    await sio_server.emit('congrateWinner', player["level"], to=player['sid'])
    await sio_server.emit('noteOpponentWon', to=player['sid'])

@sio_server.event
async def get_opponent(sid, username,room_number):
    room = await rooms_collection.find_one({"room_number" : room_number})
    opponent_name = room["player_x"] if room["player_x"] != username else room["player_o"]
    return opponent_name




@sio_server.event
async def handle_rps_click(sid, i , username, opponent_name, room_number):
    room = await rooms_collection.find_one({"room_number" : room_number})
    game_res = room.get("rps_game")
    player_choice = game_res.get(username)
    opponent_choice = game_res.get(opponent_name)
    player_won = room["winner"]
    if player_choice or player_choice == 0 or player_won:
        return False
    if opponent_choice or opponent_choice == 0:
        winner = calculate_rps_winner(i , opponent_choice)
        if winner == 'draw':
            await declare_draw(username, room_number, opponent_name)
        else:
            player = await users_collection.find_one({"username": username})
            opponent = await users_collection.find_one({"username": opponent_name})
            if winner == 0:
                await declare_winner(player, opponent, room)
            elif winner == 1:
                await declare_winner(opponent, player, room)
    game_res[username] = i
    rooms_collection.update_one({"room_number": room_number}, {"$set" : {"rps_game":game_res}})
    return True


@sio_server.event
async def get_game(sid, username):
    user = await users_collection.find_one({"username": username})
    room = await rooms_collection.find_one({"room_number": user["room_number"]})
    return room['game_type']

@sio_server.event
async def update_joined(sid, username, value):
    await users_collection.update_one({"username": username}, {"$set" : {"joined": value}})
    players = await get_connected_players()
    await sio_server.emit('setPlayers', players)
