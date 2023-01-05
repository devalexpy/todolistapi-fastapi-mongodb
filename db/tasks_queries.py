from config.db_connection import db
from bson import ObjectId


async def insert_task(task: dict):
    task["user_id"] = ObjectId(task["user_id"])
    task = await db.tasks.insert_one(task)


async def find_task(task_id):
    task = await db.tasks.find_one({"_id": ObjectId(task_id)})
    return task


async def update_task(task: dict, task_id: str):
    task = await db.tasks.update_one({"_id": ObjectId(task_id)}, {"$set": task})
    return await find_task(ObjectId(task_id))


async def delete_task_by_id(task_id):
    await db.tasks.delete_one({"_id": ObjectId(task_id)})


async def get_tasks(user_id):
    tasks = await db.tasks.find({"user_id": ObjectId(user_id)}).to_list(length=100)
    return tasks
