import operator
sub = operator.sub
add = operator.add
mul = operator.mul
div = operator.truediv

def get_enemies_list(piece):
    whitelist = ["R", "N", "B", "Q", "K", "P"]
    blacklist = ["r", "n", "b", "q", "k", "p"]
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



def rook_avalible_moves(chess_board, r_index, c_index, piece):
    enemies_list = get_enemies_list(piece)
    moves = []
    enemies_king = "K" if piece == "r" else "k"
    if r_index + 1 < 8 :
        for index in range(r_index+1, 8):
            square = chess_board[index][c_index]
            if square != " ":
                if square == enemies_king:
                    continue
                if square in enemies_list :
                    moves.append((index, c_index))
                break
            moves.append((index, c_index))

    if r_index -1 >= 0 :
        for index in range(r_index-1, -1, -1):
            square = chess_board[index][c_index]
            if square != " ":
                print("[r_index][c_index] from rook attack >>>> ", [r_index, c_index])
                print("square from rook attack >>>> ", square)
                if square == enemies_king:
                    continue
                if square in enemies_list :
                    moves.append((index, c_index))
                break
            moves.append((index, c_index))

    if c_index + 1 < 8 :
        for index in range(c_index+1, 8):
            square = chess_board[r_index][index]
            if square != " ":
                if square == enemies_king:
                    continue
                if square in enemies_list :
                    moves.append((r_index, index))
                break
            moves.append((r_index, index))
            
    if c_index -1 >= 0 :
        for index in range(c_index-1, -1, -1):
            square = chess_board[r_index][index]
            if square != " ":
                if square == enemies_king:
                    continue
                if square in enemies_list :
                    moves.append((r_index, index))
                break
            moves.append((r_index, index))
    return moves


def bishop_avalible_moves(chess_board, r_index, c_index, piece):
    enemies_list = get_enemies_list(piece)
    moves = []
    enemies_king = "K" if piece == "b" else "k"
    pp_counter = 0
    for index in range(min([r_index, c_index])+1, 8):
        pp_counter += 1
        temp_r_index = r_index+pp_counter
        temp_c_index = c_index+pp_counter
        if temp_r_index == 8 or temp_c_index == 8 :
            break
        square = chess_board[temp_r_index][temp_c_index]
        if square != " ":
            if square == enemies_king:
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
            if square == enemies_king:
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
            if square == enemies_king:
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
            if square == enemies_king:
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
    moves = []

    if c_index + 2 < 8:
        if r_index < 7 :
            square = chess_board[r_index+1][c_index+2]
            if square == " " or square in enemies_list:
                moves.append((r_index+1, c_index+2))
        if r_index > 0 :
            square = chess_board[r_index-1][c_index+2]
            if square == " " or square in enemies_list:
                moves.append((r_index-1, c_index+2))
    if c_index - 2 > -1:
        if r_index < 7 :
            square = chess_board[r_index+1][c_index-2]
            if square == " " or square in enemies_list:
                moves.append((r_index+1, c_index-2))
        if r_index > 0 :
            square = chess_board[r_index-1][c_index-2]
            if square == " " or square in enemies_list:
                moves.append((r_index-1, c_index-2))

    if r_index + 2 < 8:
        if c_index < 7 :
            square = chess_board[r_index+2][c_index+1]
            if square == " " or square in enemies_list:
                moves.append((r_index+2, c_index+1))
        if c_index > 0 :
            square = chess_board[r_index+2][c_index-1]
            if square == " " or square in enemies_list:
                moves.append((r_index+2, c_index-1))

    if r_index - 2 > -1:
        if c_index < 7 :
            square = chess_board[r_index-2][c_index+1]
            if square == " " or square in enemies_list:
                moves.append((r_index-2, c_index+1))
        if c_index > 0 :
            square = chess_board[r_index-2][c_index-1]
            if square == " " or square in enemies_list:
                moves.append((r_index-2, c_index-1))

    return moves


def king_avalible_moves(chess_board, r_index, c_index, piece):
    enemies_list = get_enemies_list(piece)
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
    safe_from_pawns = is_safe_from_pawns(chess_board, index_r, index_c, piece)
    if not safe_from_pawns :
        return False
    
    safe_from_rooks = is_safe_from_rooks(chess_board, index_r, index_c, piece)
    if not safe_from_rooks :
        return False
    
    safe_from_bishop = is_safe_from_bishop(chess_board, index_r, index_c, piece)
    if not safe_from_bishop :
        return False
    
    safe_from_knight = is_safe_from_knight(chess_board, index_r, index_c, piece)
    if not safe_from_knight :
        return False
    
    return True
    

def is_safe_from_pawns(chess_board, r_index, c_index, piece):
    enemies_list = get_enemies_list(piece)
    if piece == "K":
        threatlist = [
            [r_index-1, c_index+1],
            [r_index-1, c_index-1]
        ]
    if piece == "k":
        threatlist = [
            [r_index+1, c_index+1],
            [r_index+1, c_index-1]
        ]
    for cordinates in threatlist:
        index_r = cordinates[0]
        index_c = cordinates[1]
        if index_r in range(0,8) and index_c in range(0,8):
            square = chess_board[index_r][index_c]
            if square in enemies_list:
                return False
    return True

def is_safe_from_rooks(chess_board, r_index, c_index, piece):
    if piece == "K":
        rook_piece = "R"
        rook_queen = ["r", "q"]
    if piece == "k":
        rook_piece = "r"
        rook_queen = ["R", "Q"]
    rook_moves = rook_avalible_moves(chess_board, r_index, c_index, rook_piece)
    for cordinates in rook_moves:
        index_r = cordinates[0]
        index_c = cordinates[1]
        square = chess_board[index_r][index_c]
        if square in rook_queen:
            return False
    return True

def is_safe_from_bishop(chess_board, r_index, c_index, piece):
    if piece == "K":
        bishop_piece = "B"
        bishop_queen = ["b", "q"]
    if piece == "k":
        bishop_piece = "b"
        bishop_queen = ["B", "Q"]
    bishop_moves = bishop_avalible_moves(chess_board, r_index, c_index, bishop_piece)
    for cordinates in bishop_moves:
        index_r = cordinates[0]
        index_c = cordinates[1]
        square = chess_board[index_r][index_c]
        if square in bishop_queen:
            return False
    return True


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
            return False
    return True