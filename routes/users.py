# Models
from models.user import(
    UserSingUp, UserOut, UserLogin,
    UserUpdateBasicInfo, UserUpdatePassword
)
# Queries
from db.users_queries import(
    insert_user, find_user, update_user,
    delete_user
)
# Authentication
from passlib.context import CryptContext
# FastApi
from fastapi import(
    APIRouter, Body, HTTPException,
    status, Path
)

users = APIRouter()

pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@users.post(
    path="/users",
    summary="Register a new user",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    tags=["users"]
)
async def user_signup(user: UserSingUp = Body(...)):
    user.password = pass_context.hash(user.password)
    created_user = await insert_user(user.dict())
    if created_user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )
    created_user.pop("password")
    return created_user


@users.post(
    path="/users/login",
    summary="Login a user",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    tags=["users"]
)
async def user_login(user: UserLogin = Body(...)):
    user_data = await find_user(user.username)
    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    if not pass_context.verify(user.password, user_data["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    else:
        return user_data


@users.put(
    path="/users/{user_id}/updateBasicInfo",
    summary="Update basic info of the user",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    tags=["users"]
)
async def user_basic_info_update(user: UserUpdateBasicInfo = Body(...), user_id: str = Path(...)):
    user = {key: value for key, value in user.dict().items()
            if value is not None}
    user_updated = await update_user(user, user_id)
    return user_updated


@users.put(
    path="/users/{user_id}/updatePassword",
    summary="Update the password of the user",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    tags=["users"]
)
async def password_update(usar_pass: UserUpdatePassword = Body(...), user_id: str = Path(...)):
    user = await find_user(user_id)
    if not pass_context.verify(usar_pass.old_password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
    new_password = pass_context.hash(usar_pass.new_password)
    user_updated = await update_user({"password": new_password}, user_id)
    return user_updated


@users.delete(
    path="/users/{user_id}/delete",
    summary="Delete a user",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    tags=["users"]
)
async def user_delete(user_id: str = Path(...)):
    user_deleted = await delete_user(user_id)
    return user_deleted
