from .server import sio_app, sio_server
from config.db import users_collection, rule_collection, rooms_collection, msgs_collection
from .chess_calc import *
base_board = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"]
]


def get_player_turn_chess(room, chess_moves, username):
    player_turn = "player_x" if chess_moves % 2 == 0 else "player_o"
    return room[player_turn] == username


def get_player_color(room, piece, username):
    player_type = "player_x" if piece in ["R", "N", "B", "Q", "K", "P"] else "player_o"
    return room[player_type] == username



def available_moves(chess_board, r_index, c_ndex, piece):
    if piece in ["P", "p"]:
        return pawn_available_moves(chess_board, r_index, c_ndex, piece)
    if piece in ["R", "r"]:
        return rook_available_moves(chess_board, r_index, c_ndex, piece)
    if piece in ["B", "b"]:
        return bishop_available_moves(chess_board, r_index, c_ndex, piece)
    if piece in ["Q", "q"]:
        return queen_available_moves(chess_board, r_index, c_ndex, piece)
    if piece in ["N", "n"]:
        return knight_available_moves(chess_board, r_index, c_ndex, piece)
    if piece in ["K", "k"]:
        return king_available_moves(chess_board, r_index, c_ndex, piece)
    return False



