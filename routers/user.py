from fastapi import APIRouter
from fastapi.responses import JSONResponse

from models.user import User
from utils.jwt_manager import create_token

user_router = APIRouter()


@user_router.post("/login", tags=['Auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.model_dump())
        return JSONResponse(content={"jwt": token})
