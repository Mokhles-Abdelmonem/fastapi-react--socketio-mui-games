from .chess_utils import * 

@sio_server.event
async def get_chess_board(sid, username):
        user = await users_collection.find_one({"username": username})
        room = await rooms_collection.find_one({"room_number": user["room_number"]})
        return room["chess_board"]

@sio_server.event
async def get_avalible_moves(sid, username, r_index, c_ndex, piece):
    player = await users_collection.find_one({"username": username})
    room_number = player['room_number']
    room = await rooms_collection.find_one({"room_number": room_number})
    chess_moves = room["chess_moves"]
    player_turn = get_player_turn_chess(room, chess_moves, username)
    player_color = get_player_color(room, piece, username)
    if not player_turn or not player_color:
        return False
    chess_board = room["chess_board"]
    moves = avalible_moves(chess_board, r_index, c_ndex, piece)
    return {"avalible_moves":moves, "highlightPiece":[r_index, c_ndex]}
    move_valid = check_move_validation(chess_board, r_index, c_ndex, piece)
    chess_moves += 1
    rooms_collection.update_one({"room_number": room_number},{"$set": {"chess_moves":chess_moves}})

