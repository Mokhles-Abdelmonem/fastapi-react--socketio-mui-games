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


async def get_joined_players():
    players_list = []
    players = users_collection.find({"joined" : True})
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