from config.db_connection import db
from pymongo.errors import DuplicateKeyError
from bson import ObjectId


async def insert_user(user: dict):
    try:
        await db.users.insert_one(user)
    except DuplicateKeyError:
        return None
    else:
        return await db.users.find_one({"username": user["username"]})


async def find_user(username):
    user = await db.users.find_one({"username": username})
    return user


async def update_user(user_data, user_id):
    await db.users.update_one({"_id": ObjectId(user_id)}, {"$set": user_data})
    return await db.users.find_one({"_id": ObjectId(user_id)})


async def delete_user(user_id):
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    await db.users.delete_one({"_id": ObjectId(user_id)})
    return user
