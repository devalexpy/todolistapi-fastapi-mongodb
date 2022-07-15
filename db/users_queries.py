from config.db_connection import db
from pymongo.errors import DuplicateKeyError


async def insert_user(user: dict):
    try:
        await db.users.insert_one(user)
    except DuplicateKeyError:
        return None
    else:
        return user


async def find_user(user_id="", username=""):
    user = await db.users.find_one({"$or": [{"_id": user_id}, {"username": username}]})
    return user


async def update_user(user_data, user_id):
    await db.users.update_one({"_id": user_id}, {"$set": user_data})
    update_user = await db.users.find_one({"_id": user_id})
    return update_user


async def delete_user(user_id):
    user_deleted = await db.users.find_one({"_id": user_id})
    await db.users.delete_one({"_id": user_id})
    return user_deleted
