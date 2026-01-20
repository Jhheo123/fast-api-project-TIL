from datetime import datetime
import time

from fastapi import APIRouter

router = APIRouter(prefix = "/sync-test")

def sync_task(num): # 동기식 동작 작업 정의
    print("sync_task: ", num)
    time.sleep(1) # 작업 걸리는 시간 테스트
    return num

@router.get("")
def sync_example():
    now = datetime.now()
    results = [sync_task(1), sync_task(2), sync_task(3)] # 순차적 실행
    print(datetime.now() - now) # 작업 수행 시간 측정
    return {"results": results}
