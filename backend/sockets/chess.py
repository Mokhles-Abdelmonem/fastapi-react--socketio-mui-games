from .chess_utils import * 
from .utils import declare_winner, switch_timer, declare_draw
@sio_server.event
async def get_chess_board(sid, username):
        user = await users_collection.find_one({"username": username})
        room = await rooms_collection.find_one({"room_number": user["room_number"]})
        return {"chess_board":room["board_history"][-1], "check":room["check"]}

@sio_server.event
async def get_available_moves(sid, username, r_index, c_index, piece):
    player = await users_collection.find_one({"username": username})
    room_number = player['room_number']
    room = await rooms_collection.find_one({"room_number": room_number})
    chess_moves = room["chess_moves"]
    player_turn = get_player_turn_chess(room, chess_moves, username)
    player_color = get_player_color(room, piece, username)
    mate = room["mate"]
    winner = room["winner"]
    draw = room.get("draw")
    if not player_turn or not player_color or mate or winner or draw:
        return False
    chess_history = room["board_history"]
    chess_board = chess_history[-1]
    casel_context = {
    "check" : room["check"],
    "K_moved" : room["K_moved"],
    "k_moved" : room["k_moved"],
    "R_0_moved" : room["R_0_moved"],
    "r_0_moved" : room["r_0_moved"],
    "R_7_moved" : room["R_7_moved"],
    "r_7_moved" : room["r_7_moved"]
    }

    passent_context = {
    "en_passant" : room["en_passant"],
    "en_passant_to" : room["en_passant_to"]
    }

    moves = available_moves(chess_board, r_index, c_index, piece, casel_context, passent_context)
    if piece not in ['K', 'k']:
        enemies_list = get_enemies_list(piece)
        if "p" in enemies_list:
            king_position = room["white_king_position"]
        if "P" in enemies_list:
            king_position = room["black_king_position"]

        pinned, pinned_moves = check_piece_is_pinned(chess_board, r_index, c_index, piece, king_position)
        if pinned and moves :
            aval_moves = []
            for move in pinned_moves :
                if move in moves :
                    aval_moves.append(move)
            moves = aval_moves
        forced_moves = room["forced_moves"]
        if forced_moves and moves:
            new_moves = []
            for move in forced_moves :
                if move in moves :
                    new_moves.append(move)
            moves = new_moves
        check = room["check"]
        if check and not forced_moves :
            moves = []
    return {"available_moves":moves, "highlightPiece":[r_index, c_index]}

@sio_server.event
async def submit_piece_move(sid, username, r_index, c_index, initial_r_index, initial_c_index):
    player = await users_collection.find_one({"username": username})
    room_number = player['room_number']
    room = await rooms_collection.find_one({"room_number": room_number})
    chess_history = room["board_history"] 
    chess_board = chess_history[-1]
    piece = chess_board[initial_r_index][initial_c_index]
    chess_moves = room["chess_moves"]
    chess_moves += 1
    room_update = {
        "chess_moves":chess_moves,
        "forced_moves":[],
        "check":None,
    }
    if piece == "K":
        
        player_side = "player_x"
        opponent_side = "player_o"
        the_king = "k"
        king_position = room["black_king_position"]

        right_square = None 
        left_square = None
        if c_index in range(2, 7) :
            right_square = chess_board[r_index][c_index+1]
            left_square = chess_board[r_index][c_index-2]
        K_moved = room["K_moved"]
        if not K_moved and (right_square == "R" or left_square == "R"):
            chess_board[initial_r_index][initial_c_index] = " "
            if c_index == 2 :
                chess_board[r_index][0] = " "
                chess_board[r_index][2] = "K"
                chess_board[r_index][3] = "R"
            elif c_index == 6 :
                chess_board[r_index][7] = " "
                chess_board[r_index][6] = "K"
                chess_board[r_index][5] = "R"
        else:
            chess_board[r_index][c_index] = piece
            chess_board[initial_r_index][initial_c_index] = " "
        room_update["white_king_position"] = [r_index, c_index]
        room_update["K_moved"] = True
        await sio_server.emit('setCheck', None, to=room_number)
    elif piece == "k":

        player_side = "player_o"
        opponent_side = "player_x"
        the_king = "k"
        king_position = room["black_king_position"]

        right_square = None 
        left_square = None
        if c_index in range(2, 7) :
            right_square = chess_board[r_index][c_index+1]
            left_square = chess_board[r_index][c_index-2]
        k_moved = room["k_moved"]
        if not k_moved and (right_square == "r" or left_square == "r"):
            chess_board[initial_r_index][initial_c_index] = " "
            if c_index == 2 :
                chess_board[r_index][0] = " "
                chess_board[r_index][2] = "k"
                chess_board[r_index][3] = "r"
            elif c_index == 6 :
                chess_board[r_index][7] = " "
                chess_board[r_index][6] = "k"
                chess_board[r_index][5] = "r"
        else:
            chess_board[r_index][c_index] = piece
            chess_board[initial_r_index][initial_c_index] = " "
        room_update["black_king_position"] = [r_index, c_index]
        room_update["k_moved"] = True
        await sio_server.emit('setCheck', None, to=room_number)
    else:

        chess_board[r_index][c_index] = piece
        chess_board[initial_r_index][initial_c_index] = " "
        enemies_list = get_enemies_list(piece)
        if "p" in enemies_list:
            player_side = "player_x"
            opponent_side = "player_o"
            the_king = "k"
            king_position = room["black_king_position"]
        if "P" in enemies_list:
            the_king = "K"
            king_position = room["white_king_position"]
            player_side = "player_o"
            opponent_side = "player_x"

        if piece == "R":
            if initial_r_index == 0:
                room_update["R_0_moved"] = True
            elif initial_r_index == 7: 
                room_update["R_7_moved"] = True
        elif piece == "r":
            if initial_r_index == 0:
                room_update["r_0_moved"] = True
            elif initial_r_index == 7: 
                room_update["r_7_moved"] = True


        en_passant_list = []
        en_passant_to = []
        en_passant_to = room["en_passant_to"]
        if piece == "P" :
            if [r_index, c_index] == en_passant_to:
                chess_board[r_index+1][c_index] = " "
            if initial_r_index - r_index == 2:
                if c_index > 0 :
                    left_square = chess_board[r_index][c_index-1]
                    if left_square == "p" :
                        en_passant_list.append([r_index, c_index-1])
                    en_passant_to = [r_index+1, c_index]
                if c_index < 7 :
                    right_square = chess_board[r_index][c_index+1]
                    if right_square == "p" :
                        en_passant_list.append([r_index, c_index+1])
                    en_passant_to = [r_index+1, c_index]
            if r_index == 0:
                chess_board[r_index][c_index] = "Q"
        elif piece == "p":
            if [r_index, c_index] == en_passant_to:
                chess_board[r_index-1][c_index] = " "
            if r_index - initial_r_index == 2:
                if c_index > 0 :
                    left_square = chess_board[r_index][c_index-1]
                    if left_square == "P" :
                        en_passant_list.append([r_index, c_index-1])
                    en_passant_to = [r_index-1, c_index]
                if c_index < 7 :
                    right_square = chess_board[r_index][c_index+1]
                    if right_square == "P" :
                        en_passant_list.append([r_index, c_index+1])
                    en_passant_to = [r_index-1, c_index]
            if r_index == 7:
                chess_board[r_index][c_index] = "q"
        room_update["en_passant"] = en_passant_list 
        room_update["en_passant_to"] = en_passant_to 

    index_r = king_position[0]
    index_c = king_position[1]
    check, available_moves , forced_moves = king_is_checked(chess_board, index_r, index_c, the_king)   
    if check :
        room_update['check'] = the_king
        room_update["forced_moves"] = forced_moves
        await sio_server.emit('setCheck', the_king, to=room_number)
        if not forced_moves and not available_moves:
            room_update['mate'] = True
            player_name = room[player_side]
            opponent_name = room[opponent_side]
            player = await users_collection.find_one({'username': player_name})
            opponent = await users_collection.find_one({'username': opponent_name})
            await declare_winner(player ,opponent , room)
    else:
        k_index_r = king_position[0]
        k_index_c = king_position[1]
        king_moves = king_available_moves(chess_board, k_index_r, k_index_c, the_king)
        if not king_moves:
            if not any_move(chess_board, piece, room):
                print("there no king_moves or any other moves")
                opponent_name = room[opponent_side]
                await declare_draw(username, room_number, opponent_name)
        await sio_server.emit('setCheck', None, to=room_number)

    draw = await check_draw(chess_board, room_number, room_update)
    if draw:
        opponent_name = room[opponent_side]
        await declare_draw(username, room_number, opponent_name)


    chess_history.append(chess_board)
    room_update["board_history"] = chess_history
    await sio_server.emit('setChessBoard', chess_board, to=room_number)
    
    chess_moves = room["chess_moves"]
    opponent_name = room[opponent_side]
    opponent = await users_collection.find_one({'username': opponent_name})
    
    
    await switch_timer(player, opponent_name, player_side)

    rooms_collection.update_one({"room_number": room_number},{"$set": room_update})




async def check_draw(chess_board, room_number, room_update):
    old_room = await rooms_collection.find_one({"room_number": room_number})
    repetition = await threefold_repetition(chess_board, old_room, room_update)
    if repetition :
        return True
    pass_fifty = await fifty_Move_rule_count(chess_board, old_room, room_update)
    if pass_fifty :
        return True
    return False

async def threefold_repetition(chess_board, old_room, room_update):
    threefold_dict = old_room["threefold_dict"]
    old_chess_history = old_room["board_history"]
    if chess_board in old_chess_history :
        threefold_count = threefold_dict.get(str(chess_board))
        if threefold_count :
            threefold_count += 1
        else:
            threefold_count = 1
        threefold_dict[str(chess_board)] = threefold_count
        room_update["threefold_dict"] = threefold_dict
        if threefold_count == 3:
            return True, room_update
    return False




async def fifty_Move_rule_count(chess_board, old_room, room_update):
    last_chess_board = old_room["board_history"][-1]
    fifty_Move_count = old_room["fifty_Move_count"]
    new_board_squares = 0
    old_board_squares = 0
    for index in range(8):
        new_board_squares += chess_board[index].count(" ")
        old_board_squares += last_chess_board[index].count(" ")
    if new_board_squares != old_board_squares:
        room_update["fifty_Move_count"] = 0
        return False
    for r_index in range(1, 8):
        for c_index in range(8):
            old_square = last_chess_board[r_index][c_index]
            if old_square in ["p", "P"]:
                square = chess_board[r_index][c_index]
                if square != old_square:
                    room_update["fifty_Move_count"] = 0
                    return False
    fifty_Move_count +=1
    room_update["fifty_Move_count"] = fifty_Move_count
    if fifty_Move_count == 50 :
        return True 
    return False

    

async def insufficient_material(chess_board, room_update):
    bishop_index_wh = 0
    bishop_count_wh = 0
    bishop_count_bl = 0
    knight_count_wh = 0
    knight_count_bl = 0
    for r_index, row in enumerate(chess_board):
        for piece in ["p", "P", "r", "R", "q", "Q"]:
            piece_count = row.count(piece)
            if piece_count > 0 :
                return False
        
        bishop_count_wh += row.count("B")
        if bishop_count_wh > 1 :
            return False
        elif bishop_count_wh == 1 :
            pass
        bishop_count_bl += row.count("b")
        if bishop_count_bl > 1 :
            return False
        knight_count_wh += row.count("N")
        if knight_count_wh > 1 :
            return False
        knight_count_bl += row.count("n")
        if knight_count_bl > 1 :
            return False
    if bishop_count_wh == 1 :
        pass

    return False