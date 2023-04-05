import operator
sub = operator.sub
add = operator.add
mul = operator.mul
div = operator.truediv



def pawn_avalible_moves(chess_board, r_index, c_ndex, piece):
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
    if chess_board[sub(r_index, 1)][c_ndex] == " ":
        moves.append((sub(r_index, 1), c_ndex))
        if r_index == start_row:
            if chess_board[sub(r_index, 2)][c_ndex] == " ":
                moves.append((sub(r_index, 2), c_ndex))
            return moves
    front_row = chess_board[sub(r_index, 1)]
    left_diagonal_player = front_row[sub(c_ndex, 1)].strip() if c_ndex != 0 else None 
    right_diagonal_player = front_row[add(c_ndex, 1)].strip() if c_ndex < len(front_row) else None 
    if left_diagonal_player:
        if left_diagonal_player in enemies_list:
            moves.append((sub(r_index, 1), sub(c_ndex, 1)))
    if right_diagonal_player:
        if right_diagonal_player in enemies_list:
            moves.append((sub(r_index, 1), add(c_ndex, 1)))
    return moves
