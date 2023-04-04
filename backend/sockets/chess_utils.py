from .server import sio_app, sio_server
from config.db import users_collection, rule_collection, rooms_collection, msgs_collection

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
