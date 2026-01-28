import asyncio

from fastapi import APIRouter, BackgroundTasks

router = APIRouter(prefix = "/bg-task-test") 
async def perform_task(task_id: int): # 백그라운드로 수행되는 작업 정의 -> 작업 id 출력
    await asyncio.sleep(3) # 3초간 대기
    print(f"{task_id}번 태스크 수행 완료! ")

@router.post("")
def create_task(task_id: int, background_tasks: BackgroundTasks): # BackgroudTasks 객체 주입
    background_tasks.add_task(perform_task, task_id) # 백그라운드 작업 추가 (태스크 수행할 함수, 그 함수에 전달할 인수)
    return {"message": "태스크가 생성되었습니다."} # 즉시 응답 보내기