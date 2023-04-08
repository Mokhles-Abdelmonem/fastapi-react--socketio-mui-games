import operator
sub = operator.sub
add = operator.add
mul = operator.mul
div = operator.truediv



def pawn_avalible_moves(chess_board, r_index, c_index, piece):
    sub = operator.sub
    add = operator.add
    if piece == "P":
        start_row = 6
        enemies_list = ["r", "n", "b", "q", "k", "p"]
    if piece == "p":
        start_row = 1
        enemies_list = ["R", "N", "B", "Q", "K", "P"]
        sub, add = add, sub
    moves = []
    if chess_board[sub(r_index, 1)][c_index] == " ":
        moves.append((sub(r_index, 1), c_index))
        if r_index == start_row:
            if chess_board[sub(r_index, 2)][c_index] == " ":
                moves.append((sub(r_index, 2), c_index))
            return moves
    front_row = chess_board[sub(r_index, 1)]
    left_diagonal_player = None
    right_diagonal_player = None
    if c_index != 0:
        left_diagonal_player = front_row[sub(c_index, 1)].strip()
        if left_diagonal_player in enemies_list:
            moves.append((sub(r_index, 1), sub(c_index, 1)))
    if c_index < len(front_row):
        right_diagonal_player = front_row[add(c_index, 1)].strip() 
        if right_diagonal_player in enemies_list:
            moves.append((sub(r_index, 1), add(c_index, 1)))
    return moves


def get_enemies_list(piece):
    whitelist = ["R", "N", "B", "Q", "K", "P"]
    blacklist = ["r", "n", "b", "q", "k", "p"]
    if piece in whitelist :
        return blacklist
    else :
        return whitelist

def rook_avalible_moves(chess_board, r_index, c_index, piece):
    enemies_list = get_enemies_list(piece)
    moves = []
    if r_index + 1 < 8 :
        for index in range(r_index+1, 8):
            square = chess_board[index][c_index]
            if square != " ":
                if square in enemies_list :
                    moves.append((index, c_index))
                break
            moves.append((index, c_index))

    if r_index -1 >= 0 :
        for index in range(r_index-1, -1, -1):
            square = chess_board[index][c_index]
            if square != " ":
                if square in enemies_list :
                    moves.append((index, c_index))
                break
            moves.append((index, c_index))

    if c_index + 1 < 8 :
        for index in range(c_index+1, 8):
            square = chess_board[r_index][index]
            if square != " ":
                if square in enemies_list :
                    moves.append((r_index, index))
                break
            moves.append((r_index, index))
            
    if c_index -1 >= 0 :
        for index in range(c_index-1, -1, -1):
            square = chess_board[r_index][index]
            if square != " ":
                if square in enemies_list :
                    moves.append((r_index, index))
                break
            moves.append((r_index, index))
    return moves


def bishop_avalible_moves(chess_board, r_index, c_index, piece):
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
            print("square  >>>>>>>>>>>>> ", square)
            if square == " " or square in enemies_list:
                moves.append((index_r, index_c))

    return moves