import operator
sub = operator.sub
add = operator.add


def get_enemies_list(piece, king=None):
    whitelist = ["P", "N", "B", "R", "Q"]
    blacklist = ["p", "n", "b", "r", "q"]

    if king :
        if piece == "K" :
            return blacklist
        elif piece == "k":
            return whitelist
        
    if piece in whitelist :
        return blacklist
    else :
        return whitelist


def pawn_available_moves(chess_board, r_index, c_index, piece, passent_context):
    enemies_list = get_enemies_list(piece)
    moves = []
    if piece == "P":
        moveslist = [[r_index-1, c_index]]
        front_square = chess_board[r_index-1][c_index]
        if r_index == 6 and front_square == " ":
            moveslist.append([r_index-2, c_index])
        eatlist = [
            [r_index-1, c_index+1],
            [r_index-1, c_index-1]
        ]
    if piece == "p":
        moveslist = [[r_index+1, c_index]]
        front_square = chess_board[r_index+1][c_index]
        if r_index == 1 and front_square == " ":
            moveslist.append([r_index+2, c_index])
        eatlist = [
            [r_index+1, c_index+1],
            [r_index+1, c_index-1]
        ]

    for cordinates in moveslist:
        index_r = cordinates[0]
        index_c = cordinates[1]
        if index_r in range(0,8) and index_c in range(0,8):
            square = chess_board[index_r][index_c]
            if square == " ":
                moves.append([index_r, index_c])

    for cordinates in eatlist:
        index_r = cordinates[0]
        index_c = cordinates[1]
        if index_r in range(0,8) and index_c in range(0,8):
            square = chess_board[index_r][index_c]
            enemies_king = "K" if piece == "p" else "k"
            if square == enemies_king:
                continue
            if square in enemies_list:
                moves.append([index_r, index_c])
    en_passant =  passent_context["en_passant"]
    en_passant_to =  passent_context["en_passant_to"]
    if [r_index, c_index] in en_passant:
        moves.append(en_passant_to)
    return moves



def rook_available_moves(chess_board, r_index, c_index, piece, pass_king=False):
    enemies_list = get_enemies_list(piece)
    moves = []
    if r_index + 1 < 8 :
        for index in range(r_index+1, 8):
            square = chess_board[index][c_index]
            if square != " ":
                if pass_king:
                    if square == pass_king:
                        continue
                if square in enemies_list :
                    moves.append([index, c_index])
                break
            moves.append([index, c_index])

    if r_index -1 >= 0 :
        for index in range(r_index-1, -1, -1):
            square = chess_board[index][c_index]
            if square != " ":
                if pass_king:
                    if square == pass_king:
                        continue
                if square in enemies_list :
                    moves.append([index, c_index])
                break
            moves.append([index, c_index])

    if c_index + 1 < 8 :
        for index in range(c_index+1, 8):
            square = chess_board[r_index][index]
            if square != " ":
                if pass_king:
                    if square == pass_king:
                        continue
                if square in enemies_list :
                    moves.append([r_index, index])
                break
            moves.append([r_index, index])
            
    if c_index -1 >= 0 :
        for index in range(c_index-1, -1, -1):
            square = chess_board[r_index][index]
            if square != " ":
                if pass_king:
                    if square == pass_king:
                        continue
                if square in enemies_list :
                    moves.append([r_index, index])
                break
            moves.append([r_index, index])
    return moves


def bishop_available_moves(chess_board, r_index, c_index, piece, pass_king=False):
    enemies_list = get_enemies_list(piece)
    moves = []
    pp_counter = 0
    for index in range(min([r_index, c_index])+1, 8):
        pp_counter += 1
        temp_r_index = r_index+pp_counter
        temp_c_index = c_index+pp_counter
        if temp_r_index == 8 or temp_c_index == 8 :
            break
        square = chess_board[temp_r_index][temp_c_index]
        if square != " ":
            if square == pass_king:
                continue
            if square in enemies_list :
                moves.append([temp_r_index, temp_c_index])
            break
        moves.append([temp_r_index, temp_c_index])

    nn_counter = 0
    for index in range(min([r_index, c_index])-1, -1, -1):
        nn_counter += 1
        temp_r_index = r_index-nn_counter
        temp_c_index = c_index-nn_counter
        if temp_r_index == -1 or temp_c_index == -1 :
            break
        square = chess_board[temp_r_index][temp_c_index]
        if square != " ":
            if square == pass_king:
                continue
            if square in enemies_list :
                moves.append([temp_r_index, temp_c_index])
            break
        moves.append([temp_r_index, temp_c_index])

    np_counter = 0
    for index in range(min([r_index, c_index])+1, 8):
        np_counter += 1
        temp_r_index = r_index-np_counter
        temp_c_index = c_index+np_counter
        if temp_r_index == -1 or temp_c_index == 8 :
            break
        square = chess_board[temp_r_index][temp_c_index]
        if square != " ":
            if square == pass_king:
                continue
            if square in enemies_list :
                moves.append([temp_r_index, temp_c_index])
            break
        moves.append([temp_r_index, temp_c_index])

    pn_counter = 0
    for index in range(min([r_index, c_index])+1, 8):
        pn_counter += 1
        temp_r_index = r_index+pn_counter
        temp_c_index = c_index-pn_counter
        if temp_r_index == 8 or temp_c_index == -1 :
            break
        square = chess_board[temp_r_index][temp_c_index]
        if square != " ":
            if square == pass_king:
                continue
            if square in enemies_list :
                moves.append([temp_r_index, temp_c_index])
            break
        moves.append([temp_r_index, temp_c_index])

    return moves


def queen_available_moves(chess_board, r_index, c_index, piece):
    rook_moves = rook_available_moves(chess_board, r_index, c_index, piece)
    bishop_moves = bishop_available_moves(chess_board, r_index, c_index, piece)
    return rook_moves + bishop_moves





def knight_available_moves(chess_board, r_index, c_index, piece):
    enemies_list = get_enemies_list(piece)
    enemies_king = "K" if piece == "n" else "k"
    moves = []
    moveslist = [
        [r_index+1, c_index+2],
        [r_index-1, c_index+2],
        [r_index+1, c_index-2],
        [r_index-1, c_index-2],
        [r_index+2, c_index+1],
        [r_index+2, c_index-1],
        [r_index-2, c_index+1],
        [r_index-2, c_index-1]
    ]

    for cordinates in moveslist:
        index_r = cordinates[0]
        index_c = cordinates[1]
        if index_r in range(0,8) and index_c in range(0,8):
            square = chess_board[index_r][index_c]
            if square == " ":
                moves.append([index_r, index_c])
            else:
                if square == enemies_king:
                    continue
                if square in enemies_list :
                    moves.append([index_r, index_c])
    return moves

def king_castle_moves(chess_board, castle_context, r_index, c_index, piece, rook):
    Rook_0_moved = castle_context[f"{rook}_0_moved"]
    Rook_7_moved = castle_context[f"{rook}_7_moved"]
    moves = []
    rook_0_next_square = [
        [r_index, 1],
        [r_index, 2],
        [r_index, 3]
    ]
    rook_7_next_square = [
        [r_index, 5],
        [r_index, 6]
    ]
    if not Rook_0_moved :
        rook_0_ready_to_castle = rook_ready_to_castle(chess_board, rook_0_next_square, 0, piece, r_index, rook)
        if rook_0_ready_to_castle :
            moves.append([r_index, 2])
    if not Rook_7_moved :
        rook_7_ready_to_castle = rook_ready_to_castle(chess_board, rook_7_next_square, 7, piece, r_index, rook)
        if rook_7_ready_to_castle :
            moves.append([r_index, 6])
    return moves

def rook_ready_to_castle(chess_board, next_square, rook_c_index, piece, r_index, rook):
    the_rook_square = chess_board[r_index][rook_c_index]
    if the_rook_square != rook:
        return False
    for cordinate in next_square :
        index_r = cordinate[0]
        index_c = cordinate[1]
        square = chess_board[index_r][index_c]
        square_safe = square_is_safe(chess_board, index_r, index_c, piece)
        rook_square_safe = square_is_safe(chess_board, index_r, rook_c_index, piece)
        if square != " " or not square_safe or not rook_square_safe:
            return False
    return True

def king_available_moves(chess_board, r_index, c_index, piece, castle_context=None):
    pawns_king = "p" if piece == "k" else "P"
    rook = "r" if piece == "k" else "R"
    enemies_list = get_enemies_list(pawns_king)
    moves = []
    moveslist = [
        [r_index+1, c_index],
        [r_index+1, c_index+1],
        [r_index+1, c_index-1],
        [r_index-1, c_index],
        [r_index-1, c_index+1],
        [r_index-1, c_index-1],
        [r_index, c_index+1],
        [r_index, c_index-1]
    ]
    for cordinates in moveslist:
        index_r = cordinates[0]
        index_c = cordinates[1]
        if index_r in range(0,8) and index_c in range(0,8):
            square = chess_board[index_r][index_c]
            if square == " " or square in enemies_list:
                if square_is_safe(chess_board, index_r, index_c, piece):
                    moves.append([index_r, index_c])

    if castle_context:
        check = castle_context["check"]
        King_moved = castle_context[f"{piece}_moved"]
        if not King_moved and not check:
            castle_moves = king_castle_moves(chess_board, castle_context, r_index, c_index, piece, rook)
            moves = moves + castle_moves
    return moves


def square_is_safe(chess_board, index_r, index_c, piece):
    functions = [
        is_safe_from_pawns, 
        is_safe_from_rooks, 
        is_safe_from_bishop, 
        is_safe_from_knight,
        is_safe_from_king
        ]
    for fun in functions :
        safe, _ = fun(chess_board, index_r, index_c, piece)
        if not safe :
            return False
    return True
    

def is_safe_from_pawns(chess_board, r_index, c_index, piece):
    if piece == "K":
        threatlist = [
            [r_index-1, c_index+1],
            [r_index-1, c_index-1]
        ]
        enemy_pawn = "p"
    elif piece == "k":
        threatlist = [
            [r_index+1, c_index+1],
            [r_index+1, c_index-1]
        ]
        enemy_pawn = "P"
    for cordinates in threatlist:
        index_r = cordinates[0]
        index_c = cordinates[1]
        if index_r in range(0,8) and index_c in range(0,8):
            square = chess_board[index_r][index_c]
            if square == enemy_pawn:
                return False, [index_r, index_c]
    return True, None

def is_safe_from_rooks(chess_board, r_index, c_index, piece):
    if piece == "K":
        rook_piece = "R"
        rook_queen = ["r", "q"]
    if piece == "k":
        rook_piece = "r"
        rook_queen = ["R", "Q"]
    rook_moves = rook_available_moves(chess_board, r_index, c_index, rook_piece, pass_king=piece)
    for cordinates in rook_moves:
        index_r = cordinates[0]
        index_c = cordinates[1]
        square = chess_board[index_r][index_c]
        if square in rook_queen:
            return False, [index_r, index_c]
    return True, None

def is_safe_from_bishop(chess_board, r_index, c_index, piece):
    if piece == "K":
        bishop_piece = "B"
        bishop_queen = ["b", "q"]
    if piece == "k":
        bishop_piece = "b"
        bishop_queen = ["B", "Q"]
    bishop_moves = bishop_available_moves(chess_board, r_index, c_index, bishop_piece, pass_king=piece)
    for cordinates in bishop_moves:
        index_r = cordinates[0]
        index_c = cordinates[1]
        square = chess_board[index_r][index_c]
        if square in bishop_queen:
            return False, [index_r, index_c]
    return True, None


def is_safe_from_knight(chess_board, r_index, c_index, piece):
    if piece == "K":
        knight_piece = "N"
        enemy_knight = "n"
    if piece == "k":
        knight_piece = "n"
        enemy_knight = "N"
    knight_moves = knight_available_moves(chess_board, r_index, c_index, knight_piece)
    for cordinates in knight_moves:
        index_r = cordinates[0]
        index_c = cordinates[1]
        square = chess_board[index_r][index_c]
        if square == enemy_knight:
            return False, [index_r, index_c]
    return True, None


def is_safe_from_king(chess_board, r_index, c_index, piece):
    moveslist = [
        [r_index+1, c_index],
        [r_index+1, c_index+1],
        [r_index+1, c_index-1],
        [r_index-1, c_index],
        [r_index-1, c_index+1],
        [r_index-1, c_index-1],
        [r_index, c_index+1],
        [r_index, c_index-1]
    ]
    if piece == "K":
        enemy_king = "k"
    elif piece == "k":
        enemy_king = "K"
    for cordinates in moveslist:
        index_r = cordinates[0]
        index_c = cordinates[1]
        if index_r in range(0,8) and index_c in range(0,8):
            square = chess_board[index_r][index_c]
            if square == enemy_king:
                return False, [index_r, index_c]
    return True, None



def king_is_checked(chess_board, index_r, index_c, piece):
    functions = [
        is_safe_from_pawns, 
        is_safe_from_rooks, 
        is_safe_from_bishop, 
        is_safe_from_knight
        ]
    counter = 0 
    cordinates = None

    for fun in functions :
        safe, attacker_cordinates = fun(chess_board, index_r, index_c, piece)
        if not safe :
            counter += 1
            if counter == 2:
                available_moves =  king_available_moves(chess_board, index_r, index_c, piece)
                return True, available_moves , []
            cordinates = attacker_cordinates
    if cordinates:
        forced_moves_list = get_forced_moves(chess_board, index_r, index_c, cordinates)
        forced_moves = get_valid_forced_moves(chess_board, piece, forced_moves_list)
        available_moves =  king_available_moves(chess_board, index_r, index_c, piece)
        return True, available_moves , forced_moves

    return False , [], []

def get_forced_moves(chess_board, index_r, index_c, cordinates):
    attacker_index_r = cordinates[0]
    attacker_index_c = cordinates[1]
    piece = chess_board[attacker_index_r][attacker_index_c]
    forced_moves_list = []
    if piece in ["N", "n"]:
        forced_moves_list.append([attacker_index_r, attacker_index_c])
        return forced_moves_list
    if attacker_index_r == index_r:
        the_range = range(min([attacker_index_c, index_c])+1, max([attacker_index_c, index_c]))
        for c_index in the_range :
            forced_moves_list.append([index_r, c_index])
        forced_moves_list.append([attacker_index_r, attacker_index_c])
    elif attacker_index_c == index_c:
        the_range = range(min([attacker_index_r, index_r])+1, max([attacker_index_r, index_r]))
        for r_index in the_range :
            forced_moves_list.append([r_index, index_c])
        forced_moves_list.append([attacker_index_r, attacker_index_c])
    else:
        the_range = range(min([attacker_index_r, index_r]), max([attacker_index_r, index_r]))
        r_counter = 0
        c_counter = 0
        for _ in the_range :
            if attacker_index_r > index_r:
                r_counter += 1
            else:
                r_counter -= 1
            if attacker_index_c > index_c:
                c_counter += 1
            else:
                c_counter -= 1
            forced_moves_list.append([index_r+r_counter, index_c+c_counter])
    return forced_moves_list

def get_valid_forced_moves(chess_board, piece, forced_moves_list):
    the_king = "K" if piece == "k" else "k"
    valid_forced_moves = []
    for cordinates in forced_moves_list:
        index_r = cordinates[0]
        index_c = cordinates[1]
        square_is_safe = check_square_safety(chess_board, index_r, index_c, the_king)
        if not square_is_safe :
            valid_forced_moves.append([index_r, index_c])
    return valid_forced_moves


def check_square_safety(chess_board, index_r, index_c, piece):
    functions = [
        is_safe_from_pawns_defend, 
        is_safe_from_rooks, 
        is_safe_from_bishop, 
        is_safe_from_knight
        ]
    counter = 0  
    for fun in functions :
        counter += 1
        safe, _ = fun(chess_board, index_r, index_c, piece)
        if not safe :
            return False
    return True


def is_safe_from_pawns_defend(chess_board, r_index, c_index, piece):
    moves = []
    square  = chess_board[r_index][c_index]
    if square != " ":
        return is_safe_from_pawns(chess_board, r_index, c_index, piece)
    if piece == "K":
        if r_index > 0:
            if chess_board[r_index-1][c_index] == "p":
                moves.append([r_index-1, c_index])
                return False, None
        if r_index-2 == 1:
            if chess_board[r_index-2][c_index] == "p":
                moves.append([r_index-2, c_index])
                return False, None

    elif piece == "k":
        if r_index < 7:
            if chess_board[r_index+1][c_index] == "P":
                moves.append([r_index+1, c_index])
                return False, None
        if r_index+2 == 6:
            if chess_board[r_index+2][c_index] == "P":
                moves.append([r_index+2, c_index])
                return False, None
    return True, None



def can_pawn_take(chess_board, r_index, c_index, piece):
    moves = []
    return True, None



def check_piece_is_pinned(chess_board, r_index, c_index, piece, king_position):
    enemies_list = get_enemies_list(piece)
    pinned, pinned_moves_rook = piece_is_pinned_rook(chess_board, r_index, c_index, enemies_list, king_position)
    if pinned :
        return True, pinned_moves_rook
    return piece_is_pinned_bishop(chess_board, r_index, c_index, enemies_list, king_position)


def piece_is_pinned_rook(chess_board, r_index, c_index, enemies_list, king_position):
    rook_queen_list = ["R", "Q", "r", "q"]
    pinned_moves = []
    if r_index == king_position[0] :
        if c_index > king_position[1] :
            for index_c in range(king_position[1]+1, c_index):
                square = chess_board[r_index][index_c]
                if square != " ":
                    return False, None
                pinned_moves.append([r_index, index_c])
            if c_index < 7:
                for index_c in range(c_index+1, 8):
                    square = chess_board[r_index][index_c]
                    if square != " ":
                        if square in enemies_list and square in rook_queen_list:
                            pinned_moves.append([r_index, index_c])
                            return True, pinned_moves
                        else:
                            return False, None
                    pinned_moves.append([r_index, index_c])
        else:
            for index_c in range(king_position[1]-1, c_index, -1):
                square = chess_board[r_index][index_c]
                if square != " ":
                    return False, None
                pinned_moves.append([r_index, index_c])
            if c_index > 0:
                for index_c in range(c_index-1, -1, -1):
                    square = chess_board[r_index][index_c]
                    if square != " ":
                        if square in enemies_list and square in rook_queen_list:
                            pinned_moves.append([r_index, index_c])
                            return True, pinned_moves
                        else:
                            return False, None
                    pinned_moves.append([r_index, index_c])
    elif c_index == king_position[1] :
        if r_index > king_position[0] :
            for index_r in range(king_position[0]+1, r_index):
                square = chess_board[index_r][c_index]
                if square != " ":
                    return False, None
                pinned_moves.append([index_r, c_index])
            if r_index < 7:
                for index_r in range(r_index+1, 8):
                    square = chess_board[index_r][c_index]
                    if square != " ":
                        if square in enemies_list and square in rook_queen_list:
                            pinned_moves.append([index_r, c_index])
                            return True, pinned_moves
                        else:
                            return False, None
                    pinned_moves.append([index_r, c_index])
        else:
            for index_r in range(king_position[0]-1, r_index, -1):
                square = chess_board[index_r][c_index]
                if square != " ":
                    return False, None
                pinned_moves.append([index_r, c_index])
            if r_index > 0:
                for index_r in range(r_index-1, -1, -1):
                    square = chess_board[index_r][c_index]
                    if square != " ":
                        if square in enemies_list and square in rook_queen_list:
                            pinned_moves.append([index_r, c_index])
                            return True, pinned_moves
                        else:
                            return False, None
                    pinned_moves.append([index_r, c_index])
    return False, None


def piece_is_pinned_bishop(chess_board, r_index, c_index, enemies_list, king_position):
    if ((r_index-king_position[0])**2 != (c_index-king_position[1])**2):
        return False, None
    bishop_queen_list = ["B", "Q", "b", "q"]
    pinned_moves = []
    counter = 0
    min_range = min([king_position[1], c_index])
    max_range = max([king_position[1], c_index])
    for _ in range(min_range, max_range):
        counter += 1
        if r_index > king_position[0]:
            if c_index > king_position[1]:
                # piece is + + to king
                r_operator = operator.add
                c_operator = operator.add
                index_r = king_position[0] + counter
                index_c = king_position[1] + counter
                if r_index == index_r and c_index == index_c :
                    continue
                square = chess_board[index_r][index_c]
                if square != " ":
                    return False, None
                pinned_moves.append([index_r, index_c])
            else:
                # piece is + - to king 
                r_operator = operator.add
                c_operator = operator.sub
                index_r = king_position[0] + counter
                index_c = king_position[1] - counter
                if r_index == index_r and c_index == index_c :
                    continue
                square = chess_board[index_r][index_c]
                if square != " ":
                    return False, None
                pinned_moves.append([index_r, index_c])
        else:
            if c_index > king_position[1]:
                # piece is - + to king 
                r_operator = operator.sub
                c_operator = operator.add
                index_r = king_position[0] - counter
                index_c = king_position[1] + counter
                if r_index == index_r and c_index == index_c :
                    continue
                square = chess_board[index_r][index_c]
                if square != " ":
                    return False, None
                pinned_moves.append([index_r, index_c])
            else:
                # piece is - - to king
                index_r = king_position[0] - counter
                index_c = king_position[1] - counter
                r_operator = operator.sub
                c_operator = operator.sub
                if r_index == index_r and c_index == index_c :
                    continue    
                square = chess_board[index_r][index_c]
                if square != " ":
                    return False, None
                pinned_moves.append([index_r, index_c])

    new_counter = 0
    while True:
        new_counter += 1
        index_r = r_operator(r_index, new_counter)
        index_c = c_operator(c_index, new_counter)
        if index_r in range(0, 8) and index_c in range(0, 8):
            square = chess_board[index_r][index_c]
            if square != " ":
                if square in enemies_list and square in bishop_queen_list:
                    pinned_moves.append([index_r, index_c])
                    return True, pinned_moves
                else:
                    return False, None
            pinned_moves.append([index_r, index_c])
        else:
            return  False, None


def available_moves(chess_board, r_index, c_ndex, piece, casel_context, passent_context):
    if piece in ["P", "p"]:
        return pawn_available_moves(chess_board, r_index, c_ndex, piece, passent_context)
    if piece in ["R", "r"]:
        return rook_available_moves(chess_board, r_index, c_ndex, piece)
    if piece in ["B", "b"]:
        return bishop_available_moves(chess_board, r_index, c_ndex, piece)
    if piece in ["Q", "q"]:
        return queen_available_moves(chess_board, r_index, c_ndex, piece)
    if piece in ["N", "n"]:
        return knight_available_moves(chess_board, r_index, c_ndex, piece)
    if piece in ["K", "k"]:
        return king_available_moves(chess_board, r_index, c_ndex, piece, casel_context)
    return False




def any_move(chess_board, piece, room):
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
    king = None
    if piece in ["K", "k"]:
        king = True
    enemies_list = get_enemies_list(piece, king)
    for piece in enemies_list:
        for r_index, row in enumerate(chess_board):
            if piece in row:
                for c_index, square in enumerate(row) :
                    if square == piece :
                        moves = available_moves(chess_board, r_index, c_index, piece, casel_context, passent_context)
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
                        if moves :
                            return True
    return False




async def check_draw(chess_board, old_room, room_update):
    repetition = await threefold_repetition(chess_board, old_room, room_update)
    if repetition :
        return True
    pass_fifty = await fifty_Move_rule_count(chess_board, old_room, room_update)
    if pass_fifty :
        return True
    insufficient_material = await Insufficient_Material(chess_board)
    if insufficient_material:
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

    

async def Insufficient_Material(chess_board):
    bishop_r_count_wh = 0
    bishop_r_count_bl = 0
    knight_r_count_wh = 0
    knight_r_count_bl = 0
    bishop_cordinates_wh = []
    bishop_cordinates_bl = []
    knight_cordinates_wh = []
    knight_cordinates_bl = []
    for r_index, row in enumerate(chess_board):
        for piece in ["p", "P", "r", "R", "q", "Q"]:
            if piece in row:
                piece_count = row.count(piece)
                if piece_count > 0 :
                    return False
        if "B" in row:
            bishop_r_count_wh += row.count("B")
            if bishop_r_count_wh > 1 :
                return False
            elif bishop_r_count_wh == 1 :
                bishop_cordinates_wh = [r_index, row.index("B")]

        if "b" in row:
            bishop_r_count_bl += row.count("b")
            if bishop_r_count_bl > 1 :
                return False
            elif bishop_r_count_bl == 1 :
                bishop_cordinates_bl = [r_index, row.index("b")]
        if "N" in row:
            knight_r_count_wh += row.count("N")
            if knight_r_count_wh > 1 :
                return False
            elif knight_r_count_wh == 1 :
                knight_cordinates_wh = [r_index, row.index("N")]
        if "n" in row:
            knight_r_count_bl += row.count("n")
            if knight_r_count_bl > 1 :
                return False
            elif knight_r_count_bl == 1 :
                knight_cordinates_bl = [r_index, row.index("n")]
    if bishop_cordinates_wh and knight_cordinates_wh :
        return False
    if bishop_cordinates_bl and knight_cordinates_bl :
        return False
    if bishop_cordinates_wh and knight_cordinates_bl :
        return False
    if bishop_cordinates_bl and knight_cordinates_wh :
        return False
    if bishop_cordinates_wh and bishop_cordinates_bl :
        wh_bishop_square_color = (bishop_cordinates_wh[0]+bishop_cordinates_wh[1])%2 == 0
        bl_bishop_square_color = (bishop_cordinates_bl[0]+bishop_cordinates_bl[1])%2 == 0
        if wh_bishop_square_color != bl_bishop_square_color:
            return False

    return True