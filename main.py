# FastApi imports
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
# Route imports
from routes import users, tasks

app = FastAPI()

app.include_router(users.router)
app.include_router(tasks.router)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")
