from .chess_utils import * 

@sio_server.event
async def get_chess_board(sid, username):
        user = await users_collection.find_one({"username": username})
        room = await rooms_collection.find_one({"room_number": user["room_number"]})
        return room["chess_board"]

@sio_server.event
async def get_avalible_moves(sid, username, r_index, c_index, piece):
    player = await users_collection.find_one({"username": username})
    room_number = player['room_number']
    room = await rooms_collection.find_one({"room_number": room_number})
    chess_moves = room["chess_moves"]
    player_turn = get_player_turn_chess(room, chess_moves, username)
    player_color = get_player_color(room, piece, username)
    if not player_turn or not player_color:
        return False
    chess_board = room["chess_board"]
    moves = avalible_moves(chess_board, r_index, c_index, piece)
    return {"avalible_moves":moves, "highlightPiece":[r_index, c_index]}

@sio_server.event
async def submit_piece_move(sid, username, r_index, c_index, initial_r_index, initial_c_index):
    player = await users_collection.find_one({"username": username})
    room_number = player['room_number']
    room = await rooms_collection.find_one({"room_number": room_number})
    chess_board = room["chess_board"]
    piece = chess_board[initial_r_index][initial_c_index]
    chess_board[r_index][c_index] = piece
    chess_board[initial_r_index][initial_c_index] = " "
    chess_moves = room["chess_moves"]
    chess_moves += 1
    room_update = {
        "chess_moves":chess_moves,
        "chess_board":chess_board
    }
    if piece == "K":
        room_update["white_king_position"] = [r_index, c_index]
    elif piece == "k":
        room_update["black_king_position"] = [r_index, c_index]
    else:
        enemies_list = get_enemies_list(piece)
        if "k" in enemies_list:
            the_king = "k"
            king_position = room["black_king_position"]
        if "K" in enemies_list:
            the_king = "K"
            king_position = room["white_king_position"]
        index_r = king_position[0]
        print("king_position << -_- >>" , king_position)
        index_c = king_position[1]
        check, avalible_moves_after_check = king_is_checked(chess_board, index_r, index_c, the_king)   
        # print("check << -_________________- >>" , check)
        # print("avalible_moves_after_check >>>>>>>>>>>>>> ", avalible_moves_after_check)
    await sio_server.emit('setChessBoard', chess_board, to=room_number)
    rooms_collection.update_one({"room_number": room_number},{"$set": room_update})
