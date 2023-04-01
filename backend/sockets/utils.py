from .server import sio_app, sio_server
from config.db import users_collection, rule_collection, rooms_collection, msgs_collection




async def countdown_disconnected_user(user):
    time = 15
    connected = False
    opponent_name = ''
    username = user["username"]
    player_room = user["room_number"]
    # player_list = room_dict.get(player_room)
    # if player_list:
    #     for player_name in player_list:
    #         if player_name != username:
    #             opponent_name = player_name

    # while time and not connected:
    #     await sio_server.sleep(1)
    #     time -= 1
    #     player = get_player(username)
    #     opponent = get_player(opponent_name)
    #     if time == 0:        
    #         if player_list:
    #             if not opponent['player_draw'] and not opponent['player_lost'] and not opponent['player_won']:
    #                 await sio_server.emit('declareWinner', {'winner': opponent_name, 'roomNumber':opponent["room_number"]})
    #                 await sio_server.emit('noteOpponentWon', to=opponent['sid'])
    #                 await sio_server.emit('congrateWinner', opponent, to=opponent['sid'])
    #         if opponent:
    #             await sio_server.emit('setDisconnectedPlayer', username, to=opponent['sid'])
    #             await sio_server.emit('notePlayerLeft', to=opponent['sid'])
    #             await stop_time_back(player_room)
    #     player = await users_collection.find_one({"username":username})
    #     connected = player['connected']


def player_helper(player):
    player.pop("_id")
    return player


async def get_connected_players():
    players_list = []
    players = users_collection.find({"connected" : True})
    async for player in players:
        player_name = player['username'] 
        if not player['in_room']:
            players_list.append(player_name)
    return players_list


async def get_chat_messages():
    msgs = msgs_collection.find({'type': 'chat'})
    messages = []
    async for message in msgs:
        message.pop('_id')
        messages.append(message)
    return messages


async def retrieve_rules():
    rules = []
    async for rule in rule_collection.find():
        rules.append(rule["winning_number"])
    return rules


async def start_rock_paper_scissor_game():
    pass



async def countdown_x(player_name, room_number, opponent_name):
    await rooms_collection.update_one({"room_number":room_number},{"$set" : {"x_turn": True}})
    x_time , x_turn, winner, room = await get_timer_data(room_number, "x_time")
    while x_turn and x_time >= 0 and not winner:
        player = await users_collection.find_one({'username': player_name})
        opponent = await users_collection.find_one({'username': opponent_name})
        print("countdown for player " + str(player_name) + str(x_time))
        await sio_server.sleep(1)
        mins, secs = divmod(x_time, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        await sio_server.emit('setTimer', timer, to=player['sid'])
        x_time -= 1
        if x_time == -1:
            await declare_winner(opponent, player, room)
        x_turn, winner, room = await get_timer_data(room_number)

async def countdown_o(player_name, room_number, opponent_name):
    await rooms_collection.update_one({"room_number":room_number},{"$set" : {"x_turn": False}})
    o_time , x_turn, winner, room = await get_timer_data(room_number, "o_time")
    while not x_turn and o_time >= 0 and not winner:
        player = await users_collection.find_one({'username': player_name})
        opponent = await users_collection.find_one({'username': opponent_name})
        print("countdown for player " + str(player_name) + str(o_time))
        await sio_server.sleep(1)
        mins, secs = divmod(o_time, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        await sio_server.emit('setTimer', timer, to=player['sid'])
        o_time -= 1
        if o_time == -1:
            await declare_winner(opponent, player, room)
        x_turn, winner, room = await get_timer_data(room_number)




async def get_timer_data(room_number, x_o_time=None):
    room = await rooms_collection.find_one({'room_number': room_number})
    x_turn = room.get("x_turn")
    winner = room.get("winner")
    if x_o_time:
        time = room.get(x_o_time)
        return time, x_turn, winner, room
    return x_turn, winner, room


async def declare_winner(winner, opponent, room):
    win_number = winner.get('win_number')
    player_level = winner.get('level')
    if not player_level:
        winner['level'] = 1
    rule = room.get("rule")
    if win_number != None:
        if win_number >= 0: 
            winner['win_number'] += 1
            if winner['win_number'] % rule == 0 :
                winner['level'] += 1
    else:
        winner['win_number'] = 0

    winner['player_won'] = True
    opponent['player_lost'] = True
    room_number = room["room_number"]
    rooms_collection.update_one({"room_number" : room_number}, {"$set" : {"winner": winner["username"]}})
    users_collection.update_one({"username" : winner["username"]}, {"$set" : winner})
    users_collection.update_one({"username" : opponent["username"]}, {"$set" : opponent})
    await sio_server.emit('declareWinner', {'winner': winner["username"], 'roomNumber':room_number})
    await sio_server.emit('congrateWinner', winner['level'], to=winner['sid'])
    await sio_server.emit('noteOpponent', opponent['level'] , to=opponent['sid'])



async def switch_timer(player, opponent_name, player_turn):
    if player_turn == 'player_x':
        sio_server.start_background_task(countdown_o, opponent_name , player["room_number"], player["username"])
    elif player_turn == 'player_o':
        sio_server.start_background_task(countdown_x, opponent_name, player["room_number"], player["username"])








async def stop_time_back(room_number):
    # await sio_server.emit('stopTimer', to=room_number)
    pass



def calculate_winner(squares, rules):

    if squares:
        for line in rules:
            x_indexes = [index for index in line if squares[index] == 'X']
            o_indexes = [index for index in line if squares[index] == 'O']
            if x_indexes == line:
                return 'X'
            elif o_indexes == line:
                return 'O'
        nulls = count_null(squares)
        if not nulls:
            return 'tie'
    return None


initial_squares = [None for i in range(9)]

def get_player_turn(squares):
    counter = count_null(squares)
    return "player_o" if counter % 2 == 0 else "player_x"



def count_null(squares):
    return squares.count(None)


def calculate_rps_winner(choise1, choise2):
    if choise1 == choise2:
        return 'draw'
    if choise1 == 0 and choise2 == 2:
        choise1 = 3        
    if choise2 == 0 and choise1 == 2:
        choise2 = 3
    choises = [choise1, choise2]
    return choises.index(max(choises))

