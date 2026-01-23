from dataclasses import dataclass
from datetime import datetime

@dataclass
class Tag:
    id: str
    name: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Note:
    id: str
    user_id: str
    title: str # 노트 제목
    content: str # 세부 내용
    memo_date: str # 해당 지식을 얻은 날짜
    tags:list[Tag] # 해시태크
    created_at: datetime
    updated_at: datetime