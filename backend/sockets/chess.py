from .chess_utils import * 
from .utils import declare_winner
@sio_server.event
async def get_chess_board(sid, username):
        user = await users_collection.find_one({"username": username})
        room = await rooms_collection.find_one({"room_number": user["room_number"]})
        return {"chess_board":room["chess_board"], "check":room["check"]}

@sio_server.event
async def get_available_moves(sid, username, r_index, c_index, piece):
    player = await users_collection.find_one({"username": username})
    room_number = player['room_number']
    room = await rooms_collection.find_one({"room_number": room_number})
    chess_moves = room["chess_moves"]
    player_turn = get_player_turn_chess(room, chess_moves, username)
    player_color = get_player_color(room, piece, username)
    mate = room["mate"]
    if not player_turn or not player_color or mate:
        return False
    chess_board = room["chess_board"]
    moves = available_moves(chess_board, r_index, c_index, piece)
    if piece not in ['K', 'k']:
        enemies_list = get_enemies_list(piece)
        if "p" in enemies_list:
            king_position = room["white_king_position"]
        if "P" in enemies_list:
            king_position = room["black_king_position"]

        pinned, pinned_moves = check_piece_is_pinned(chess_board, r_index, c_index, piece, king_position)
        if pinned :
            print("pinned_moves moves are >>>>>>>> ", pinned_moves)
        forced_moves = room["forced_moves"]
        if forced_moves and moves:
            new_moves = []
            for move in forced_moves :
                if move in moves :
                    new_moves.append(move)
            moves = new_moves
            print("new_moves moves are >>>>>>>> ", new_moves)
    return {"available_moves":moves, "highlightPiece":[r_index, c_index]}

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
        "chess_board":chess_board,
        "forced_moves":[],
        "check":None,

    }
    if piece == "K":
        room_update["white_king_position"] = [r_index, c_index]
        await sio_server.emit('setCheck', None, to=room_number)
    elif piece == "k":
        room_update["black_king_position"] = [r_index, c_index]
        await sio_server.emit('setCheck', None, to=room_number)
    else:
        enemies_list = get_enemies_list(piece)
        if "p" in enemies_list:
            player = "player_x"
            opponent = "player_o"
            the_king = "k"
            king_position = room["black_king_position"]
        if "P" in enemies_list:
            the_king = "K"
            king_position = room["white_king_position"]
            player = "player_o"
            opponent = "player_x"

        index_r = king_position[0]
        print("king_position << -_- >>" , king_position)

        index_c = king_position[1]
        check, available_moves , forced_moves = king_is_checked(chess_board, index_r, index_c, the_king)   
        if check :
            room_update['check'] = the_king
            room_update["forced_moves"] = forced_moves
            print("forced_moves << ?????????? >>" , forced_moves)
            await sio_server.emit('setCheck', the_king, to=room_number)
            if not forced_moves and not available_moves:
                print("<<<<<<<<<<<<<<<<<<<<<< King is Mate >>>>>>>>>>>>>>>>> ")
                room_update['mate'] = True
                player_name = room[player]
                opponent_name = room[opponent]
                player = await users_collection.find_one({'username': player_name})
                opponent = await users_collection.find_one({'username': opponent_name})
                await declare_winner(opponent, player, room)
        else:
            await sio_server.emit('setCheck', None, to=room_number)


    await sio_server.emit('setChessBoard', chess_board, to=room_number)
    rooms_collection.update_one({"room_number": room_number},{"$set": room_update})
