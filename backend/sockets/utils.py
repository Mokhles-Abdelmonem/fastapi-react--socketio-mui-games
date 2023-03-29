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
    x_time , x_turn, player_won = get_timer_data(room_number, "x_time")
    while x_turn and x_time >= 0 and not player_won:
        await sio_server.sleep(1)
        player_x = users_collection.find_one({'username': player_name})
        player_o = users_collection.find_one({'username': opponent_name})
        mins, secs = divmod(x_time, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        await sio_server.emit('setTimer', timer, to=player_x['sid'])
        x_time -= 1
        if x_time == -1:
            await sio_server.emit('TimeOut', to=room_number)
            # await declare_winner_back(player_o['sid'], player_o, player_x['username'])
            # await stop_time_back(room)
        x_turn, player_won = get_timer_data(room_number)


def get_timer_data(room_number, x_o_time=None):
    room = rooms_collection.find_one({'room_number': room_number})
    timer_switch = room["timer_switch"]
    x_turn = timer_switch.get("x_turn")
    player_won = timer_switch.get("player_won")
    if x_o_time:
        time = timer_switch.get(x_o_time)
        return time, x_turn, player_won
    return x_turn, player_won
    