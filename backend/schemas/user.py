def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message,
    }

def ResponseUsersList(users, current_user) -> list:
    return [user['username'] for user in users if user['username'] != current_user['username']]

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "hashed_password": user["hashed_password"],
        "joined": user["joined"],
        "in_room": user["in_room"],
        "room_number": user["room_number"],
        "sid": user["sid"],
        "side": user["side"],
        "status": user["status"],
    }


