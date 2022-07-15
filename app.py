# FastApi imports
from fastapi import FastAPI
# Route imports
from routes.users import users

app = FastAPI()

app.include_router(users)
