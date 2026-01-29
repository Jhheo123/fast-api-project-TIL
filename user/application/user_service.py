from ulid import ULID
from datetime import datetime
from user.domain.user import User
from user.domain.repository.user_repo import IUserRepository
from user.infra.repository.user_repo import UserRepository
from user.application.email_service import EmailService
from user.application.send_welcome_email_task import SendWelcomeEmailTask
from fastapi import BackgroundTasks, HTTPException, status
from utils.crypto import Crypto
from common.auth import Role, create_access_token
from database import SessionLocal 
# print("USER_SERVICE FILE:", __file__)

# 유저 서비스
class UserService:
    @inject
    def __init__(self,
                 user_repo: IUserRepository,
                 email_service: EmailService,
                 ulid: ULID,
                 crypto: Crypto,
                 send_welcome_email_task: SendWelcomeEmailTask
                 ):
        self.user_repo = user_repo # 데이터 저장을 위한 구현체
        self.ulid = ULID()
        self.crypto = Crypto()
        self.send_welcome_email_task = send_welcome_email_task
        self.email_service = email_service

    def create_user(self, 
                    # background_tasks: BackgroundTasks,
                    name: str, 
                    email: str, 
                    password: str,
                    memo: str | None = None): 

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
            password = self.crypto.encrypt(password),
            memo=memo,
            created_at = now,
            updated_at = now,
        )
        self.user_repo.save(user) # 생성된 객체를 저장소로 전달해 저장
        self.send_welcome_email_task.delay(user.email)
        # background_tasks.add_task(
        #     self.email_service.send_email, user.email
        # )
        SendWelcomeEmailTask().run(user.email)
        return user
    
    def update_user(
            self,
            user_id: str,
            name: str | None = None,
            password: str | None = None,
    ):
        user = self.user_repo.find_by_id(user_id)
        if name:
            user.name = name
        if password:
            user.password = self.crypto.encrypt(password)
        user.updated_at = datetime.now()

        self.user_repo.update(user)
        return user
    
    def get_users(self, page: int, items_per_page: int) -> tuple[int, list[User]]:
        users = self.user_repo.get_users(page, items_per_page)
        return users
    
    def delete_user(self, user_id:str):
        self.user_repo.delete(user_id)

    def login(self, email: str, password: str):
        # user = self.user_repo.find_by_email(email)
        # 1. 함수 시작 직후에 무조건 찍히는 로그
        print(f"\n[DEBUG] 로그인 시도 이메일: '{email}'") 
        
        try:
            user = self.user_repo.find_by_email(email)
        except HTTPException: # Repo가 던진 422 에러를 여기서 잡음
            user = None

        # 2. 유저 존재 여부 확인 로그
        if user is None:
            print(f"[DEBUG] DB에서 해당 이메일을 찾을 수 없습니다.")
        else:
            print(f"[DEBUG] 유저 찾음! ID: {user.id}")
        if user:
            # 이 로그가 터미널에 찍히는지 확인하세요
            print(f"--- LOGIN DEBUG ---")
            print(f"입력 이메일: {email}")
            print(f"입력 비밀번호: {password}")
            print(f"DB 해시값: {user.password}")
            is_correct = self.crypto.verify(password, user.password)
            print(f"검증 결과: {is_correct}")

        if not user or not self.crypto.verify(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="이메일 또는 비밀번호가 올바르지 않습니다.")
        
        access_token = create_access_token(
            payload = {"user_id": user.id},
            role=Role.USER,
        )

        return access_token
    