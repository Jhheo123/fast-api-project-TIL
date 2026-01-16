from fastapi import APIRouter
from pydantic import BaseModel
from user.application.user_service import UserService

router = APIRouter(prefix="/users")

class CreateUserBody(BaseModel):
    name: str
    email: str
    password: str

@router.post("", status_code=201)
def create_user(user: CreateUserBody):
    # print("PWD chars:", len(user.password))
    # print("PWD bytes:", len(user.password.encode("utf-8")))
    user_service = UserService()
    createed_user = user_service.create_user(
        name = user.name,
        email = user.email,
        password= user.password
    )
    return createed_user