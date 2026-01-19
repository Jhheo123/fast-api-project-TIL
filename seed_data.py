from database import SessionLocal
from user.infra.db_models.user import User
from datetime import datetime
from utils.crypto import Crypto
from ulid import ULID

crypto = Crypto()
ulid = ULID()

with SessionLocal() as db:
    for i in range(50):
        user = User(
            id=f"User-ID-{str(i).zfill(2)}",
            name=f"test_user_{i}",
            email=f"test_{i}@example.com",
            password=crypto.encrypt("test"),
            memo = None,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(user)
    db.commit()
    print("50명의 유저 생성이 완료되었습니다!")