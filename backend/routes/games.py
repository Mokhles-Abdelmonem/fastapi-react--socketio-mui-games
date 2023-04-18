from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from models.games import MessageJson, RuleJson, BoardJson
from utils.crud import * 
from sockets.server import sio_server
from sockets.utils import get_chat_messages

games_router = APIRouter(
    prefix="/games",
    tags=["Games"]
)



@games_router.post("/message/")
async def set_message(message: MessageJson):
    await msgs_collection.insert_one(
        {
        'message': message.text,
        'username': "Api",
        'type': 'chat'
         }
    )
    messages = await get_chat_messages()
    await sio_server.emit('chat', messages, to='general_room')
    return {f"message from Api": message.text}








@games_router.post("/rules/")
async def set_rule(rule: RuleJson):
    rules = await rule_collection.find_one({"winning_number": rule.winning_number})
    if rules:
        return JSONResponse(
        status_code=409,
        content={"rule": f"rule already exist"},
    )
    for rule_list in rule.rules:
        for number in rule_list:
            if type(number) != int or number not in range(9):
                return JSONResponse(
                status_code=501,
                content={"rule": "Invalid rule all rules must be integers and in range 0-8"},
                )  
    rule_collection.insert_one({"winning_number": rule.winning_number, "rules": rule.rules})
    return rule



@games_router.post("/set_chess_board/{room_number}")
async def set_chess_board(room_number, board: BoardJson):
    room = await rooms_collection.find_one({"room_number": str(room_number)})
    if not room:
        return {"error":"room not found for this number"}   
    chess_history = room["board_history"]
    chess_history[-1] = board.board
    room_update = {"board_history": chess_history}
    for board in chess_history :
        for row in board:
            print(row)
        print("_______________  board from history _______________")
    print("================ CHESS board history =================")
    rooms_collection.update_one({"room_number": str(room_number)},{"$set": room_update}) 
    return {f"success": "board updated successfully"}



@games_router.get("/get_chess_board/{room_number}")
async def get_chess_board(room_number):
    room = await rooms_collection.find_one({"room_number": str(room_number)}) 
    if not room:
        return {"error":"room not found for this number"}
    return {"board": room["board_history"][-1]}



