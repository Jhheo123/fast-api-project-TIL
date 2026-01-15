from ulid import ULID
from datetime import datetime
from user.domain.user import User
from user.domain.repository.user_repo import IUserRepository
from user.infra.repository.user_repo import UserRepository

# 유저 서비스
class UserService:
    def __init__(self):
        self.user_repo: IUserRepository = UserRepository()
        
