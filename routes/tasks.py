from fastapi import APIRouter, Body, Path
from models.task import TaskCreate, TaskOut, TaskUpdate, Status
from db.tasks_queries import insert_task, find_task, update_task, delete_task_by_id

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.get(
    path="/{task_id}",
    summary="Get a task by id",
    response_model=TaskOut
)
async def get_task(task_id: str = Path(...)):
    task = await find_task(task_id)
    return task


@router.post(
    path="/",
    summary="Create a new task",
)
async def create_task(TaskCreate: TaskCreate = Body(...)):
    await insert_task(TaskCreate.dict())
    return TaskCreate


@router.put(
    path="/{task_id}/updateBasicInfo",
    summary="Update a task by id",
    response_model=TaskOut
)
async def update_task_info(task_info: TaskUpdate = Body(...), task_id: str = Path(...)):
    task = await update_task(task_info.dict(exclude_none=True), task_id)
    return task


@router.put(
    path="/{task_id}/updateStatus/{status}}",
    summary="Update a task status by id",
)
async def update_task_status(status: Status = Path(...), task_id: str = Path(...)):
    task = await update_task({"status": status}, task_id)
    return {"message": "Task status updated successfully"}


@router.delete(
    path="/{task_id}",
    summary="Delete a task by id",
)
async def delete_task(task_id: str = Path(...)):
    await delete_task_by_id(task_id)
    return {"message": "Task deleted successfully"}
