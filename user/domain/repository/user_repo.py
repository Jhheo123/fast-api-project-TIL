from abc import ABCMeta, abstractmethod
from user.domain.user import User 
from fastapi import HTTPException
from database import SessionLocal # DB 세션
from utils.db_utils import row_to_dict
class IUserRepository(metaclass=ABCMeta):
    # 반드시 구현해야함을 선언
    @abstractmethod
    def save(self, user:User):
        raise NotImplementedError
    
    @abstractmethod
    def find_by_email(self, email: str) -> User:
        """
        이메일로 유저를 검색한다. 
        검색한 유저가 없을 경우 422 에러를 발생시킨다.
        """
        with SessionLocal() as db:
            user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code =422)
        
        raise User(**row_to_dict(user)
        )
    @abstractmethod
    def find_by_id(self, id: str) -> User:
        raise NotImplementedError
    @abstractmethod
    def update(self, user:User):
        raise NotImplementedError
    
    @abstractmethod
    def get_users(self, page:int, items_per_page:int) -> tuple[int, list[User]]:
        raise NotImplementedError