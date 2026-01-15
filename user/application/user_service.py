from ulid import ULID
from datetime import datetime
from user.domain.user import User
from user.domain.repository.user_repo import IUserRepository
from user.infra.repository.user_repo import UserRepository
from fastapi import HTTPException
from utils.crypto import Crypto

# 유저 서비스
class UserService:
    def __init__(self):
        self.user_repo: IUserRepository = UserRepository() # 데이터 저장을 위한 구현체
        self.ulid = ULID()
        self.crypto = Crypto()

    def create_user(self, name: str, email: str, password: str): 
        # 중복 유저 검사
        _user = None # 이미 찾은 유저 변수
        try:
            _user = self.user_repo.find_by_email(email)
        except HTTPException as e:
            if e.status_code != 422:
                raise e
        if _user:
            raise HTTPException(status_code=422) # 이미 가입한 유저일 경우 422 에러 일으키기
        
        now = datetime.now()
        user: User = User( # User 도메인 객체 생성
            id = self.ulid.generate(),
            name = name,
            email = email,
            password = self.crypto.encrypt(password), # 암호화 해서 저장
            created_at = now,
            updated_at = now,
        )
        self.user_repo.save(user) # 생성된 객체를 저장소로 전달해 저장
        return user
