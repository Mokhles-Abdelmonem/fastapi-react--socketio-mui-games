import motor.motor_asyncio 

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.MokhlesGame

users_collection = database.get_collection("users")
rule_collection = database.get_collection("rules")
rooms_collection = database.get_collection("rooms")
msgs_collection = database.get_collection("messages")