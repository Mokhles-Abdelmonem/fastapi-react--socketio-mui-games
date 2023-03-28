from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from models.games import MessageJson, RuleJson
from utils.crud import * 
from sockets.server import sio_server 

games_router = APIRouter(
    prefix="/games",
    tags=["Games"]
)



@games_router.post("/message/")
async def set_message(message: MessageJson, current_user: User = Depends(get_current_active_user)):
    global messages

    current_user.pop("_id", None)
    current_user.pop("hashed_password", None)
    messages.append(
        {'sid': current_user['sid'],
         'message': message.text,
         'player': current_user,
         'type': 'chat'
         }
    )
    await sio_server.emit('chat', messages, 'general_room')    
    return {f"message from {current_user['username']}": message.text}








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