import motor.motor_asyncio
from decouple import config

db = motor.motor_asyncio.AsyncIOMotorClient(
    config('MONGO_URI')).todolistdatabase
