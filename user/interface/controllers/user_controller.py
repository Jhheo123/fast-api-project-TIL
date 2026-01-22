from fastapi import APIRouter
from pydantic import BaseModel
from user.application.user_service import UserService
from dependency_injector.wiring import inject, Provide
from containers import Container
from fastapi import Depends
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from common.auth import CurrentUser, get_current_user, get_admin_user

router = APIRouter(prefix="/users")
class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime
    updated_at: datetime
class CreateUserBody(BaseModel):
    name: str = Field(min_length=2, max_length=32)
    email: str = Field(max_length=64)
    password: str = Field(min_length=8, max_length=32)

@router.post("", status_code=201)
@inject
def create_user(
    user: CreateUserBody,
    user_service:UserService = Depends(Provide[Container.user_service])
    )->UserResponse:
    print("PWD chars:", user.password)
    # print("PWD bytes:", len(user.password.encode("utf-8")))
    # user_service = UserService()
    createed_user = user_service.create_user(
        name = user.name,
        email = user.email,
        password= user.password
    )
    return createed_user
class UpdateUserBody(BaseModel):
    name: str | None = Field(min_length=2, max_length=32, default=None)
    password: str | None = Field(min_length=8, max_length=32, default=None)

# class UpdateUser(BaseModel):
#     name: str | None = Field(min_length=2, max_length=32, default=None)
#     password: str | None = Field(min_length=8, max_length=32, default=None)

# @router.put("/{user_id}")
# @inject
# def update_user(
#     user_id: str,
#     user: UpdateUser,
#     user_service: UserService = Depends(Provide[Container.user_service]),
# ):
#     user = user_service.update_user(
#         user_id = user_id,
#         name = user.name,
#         password = user.password,
#     )
#     return user
@router.put("", response_model=UserResponse)
@inject
def update_user(
    current_user:Annotated[CurrentUser, Depends(get_current_user)],
    body: UpdateUserBody,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    user = user_service.update_user(
        user_id=current_user.id,
        name = body.name,
        password=body.password,
    )
    return user

class GetUserResponse(BaseModel):
    total_count: int
    page:int
    users:list[UserResponse]

@router.get("")
@inject
def get_users(
    page: int = 1,
    items_per_page: int = 10,
    current_user: CurrentUser = Depends(get_admin_user),
    user_service: UserService = Depends(Provide[Container.user_service]),
)->GetUserResponse:
    total_count, users = user_service.get_users(page, items_per_page)
    return {
        "total_count":total_count,
        "page":page,
        "users":users,

    }

@router.delete("", status_code=204)
@inject
def delete_user(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    user_service.delete_user(current_user.id)

@router.post("/login")
@inject
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    access_token = user_service.login(
        email = form_data.username,
        password = form_data.password,
    )
    return {"access_token": access_token, "token_type":"bearer"}

