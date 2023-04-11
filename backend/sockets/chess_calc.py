import operator
sub = operator.sub
add = operator.add
mul = operator.mul
div = operator.truediv

def get_enemies_list(piece):
    whitelist = ["R", "N", "B", "Q", "P"]
    blacklist = ["r", "n", "b", "q", "p"]
    if piece in whitelist :
        return blacklist
    else :
        return whitelist


def pawn_avalible_moves(chess_board, r_index, c_index, piece):
    enemies_list = get_enemies_list(piece)
    moves = []
    if piece == "P":
        moveslist = [[r_index-1, c_index]]
        if r_index == 6:
            moveslist.append([r_index-2, c_index])
        eatlist = [
            [r_index-1, c_index+1],
            [r_index-1, c_index-1]
        ]
    if piece == "p":
        moveslist = [[r_index+1, c_index]]
        if r_index == 1:
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
                moves.append((index_r, index_c))

    for cordinates in eatlist:
        index_r = cordinates[0]
        index_c = cordinates[1]
        if index_r in range(0,8) and index_c in range(0,8):
            square = chess_board[index_r][index_c]
            enemies_king = "K" if piece == "p" else "k"
            if square == enemies_king:
                continue
            if square in enemies_list:
                moves.append((index_r, index_c))
    return moves



def rook_avalible_moves(chess_board, r_index, c_index, piece, pass_king=False):
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
                    moves.append((index, c_index))
                break
            moves.append((index, c_index))

    if r_index -1 >= 0 :
        for index in range(r_index-1, -1, -1):
            square = chess_board[index][c_index]
            if square != " ":
                if pass_king:
                    if square == pass_king:
                        continue
                if square in enemies_list :
                    moves.append((index, c_index))
                break
            moves.append((index, c_index))

    if c_index + 1 < 8 :
        for index in range(c_index+1, 8):
            square = chess_board[r_index][index]
            if square != " ":
                if pass_king:
                    if square == pass_king:
                        continue
                if square in enemies_list :
                    moves.append((r_index, index))
                break
            moves.append((r_index, index))
            
    if c_index -1 >= 0 :
        for index in range(c_index-1, -1, -1):
            square = chess_board[r_index][index]
            if square != " ":
                if pass_king:
                    if square == pass_king:
                        continue
                if square in enemies_list :
                    moves.append((r_index, index))
                break
            moves.append((r_index, index))
    return moves


def bishop_avalible_moves(chess_board, r_index, c_index, piece, pass_king=False):
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
                moves.append((temp_r_index, temp_c_index))
            break
        moves.append((temp_r_index, temp_c_index))

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
                moves.append((temp_r_index, temp_c_index))
            break
        moves.append((temp_r_index, temp_c_index))

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
                moves.append((temp_r_index, temp_c_index))
            break
        moves.append((temp_r_index, temp_c_index))

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
                moves.append((temp_r_index, temp_c_index))
            break
        moves.append((temp_r_index, temp_c_index))

    return moves


def queen_avalible_moves(chess_board, r_index, c_index, piece):
    rook_moves = rook_avalible_moves(chess_board, r_index, c_index, piece)
    bishop_moves = bishop_avalible_moves(chess_board, r_index, c_index, piece)
    return rook_moves + bishop_moves





def knight_avalible_moves(chess_board, r_index, c_index, piece):
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
                moves.append((index_r, index_c))
            else:
                if square == enemies_king:
                    continue
                if square in enemies_list :
                    moves.append((index_r, index_c))
    return moves


def king_avalible_moves(chess_board, r_index, c_index, piece):
    pawns_king = "p" if piece == "k" else "P"
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
                    moves.append((index_r, index_c))

    return moves


def square_is_safe(chess_board, index_r, index_c, piece):
    functions = [
        is_safe_from_pawns, 
        is_safe_from_rooks, 
        is_safe_from_bishop, 
        is_safe_from_knight
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
    rook_moves = rook_avalible_moves(chess_board, r_index, c_index, rook_piece, pass_king=piece)
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
    bishop_moves = bishop_avalible_moves(chess_board, r_index, c_index, bishop_piece, pass_king=piece)
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
    knight_moves = knight_avalible_moves(chess_board, r_index, c_index, knight_piece)
    for cordinates in knight_moves:
        index_r = cordinates[0]
        index_c = cordinates[1]
        square = chess_board[index_r][index_c]
        if square == enemy_knight:
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
                avalible_moves =  king_avalible_moves(chess_board, index_r, index_c, piece)
                return True, avalible_moves , []
            cordinates = attacker_cordinates
    if cordinates:
        forced_moves_list = get_forced_moves(chess_board, index_r, index_c, cordinates)
        forced_moves = get_valid_forced_moves(chess_board, piece, forced_moves_list)
        avalible_moves =  king_avalible_moves(chess_board, index_r, index_c, piece)
        return True, avalible_moves , forced_moves

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
        can_pawns_defend, 
        is_safe_from_rooks, 
        is_safe_from_bishop, 
        is_safe_from_knight
        ]
    for fun in functions :
        safe, _ = fun(chess_board, index_r, index_c, piece)
        if not safe :
            return False
    return True


def can_pawns_defend(chess_board, r_index, c_index, piece):
    moves = []
    if piece == "K":
        if chess_board[r_index-1][c_index] == "p":
            moves.append([r_index-1, c_index])
            return False, None
        if r_index-2 == 1:
            if chess_board[r_index-2][c_index] == "p":
                moves.append([r_index-2, c_index])
                return False, None

    elif piece == "k":
        if chess_board[r_index+1][c_index] == "P":
            moves.append([r_index+1, c_index])
            return False, None
        if r_index+2 == 6:
            if chess_board[r_index+2][c_index] == "P":
                moves.append([r_index+2, c_index])
                return False, None
    return True, None