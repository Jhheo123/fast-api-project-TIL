import sys
import os

# 프로젝트 루트 디렉토리를 파이썬 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from celery.result import AsyncResult
from common.messaging import celery

if __name__ == "__main__":
    async_result = AsyncResult("87d02ecc-e15e-4769-9cd5-b02283c3506f", app=celery)
    
    # .result 대신 .get() 사용 (timeout을 주면 무한 대기를 방지할 수 있습니다)
    try:
        result = async_result.get(timeout=5) 
        print(f"결과: {result}")
    except Exception as e:
        print(f"상태: {async_result.state}") # 현재 상태 확인 (PENDING, STARTED 등)
        print(f"에러 발생 또는 타임아웃: {e}")