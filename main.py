from fastapi import FastAPI
from user.interface.controllers.user_controller import router as user_routers
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from containers import Container

app = FastAPI()
container = Container()
container.wire(modules=["user.interface.controllers.user_controller"])
app.container = container

app.include_router(user_routers)

@app.exception_handler(RequestValidationError) # 422 에러가 발생했을 때 에러 핸들러 등록
async def validation_exeception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code = 400, # 응답코드 400으로 변경
        content=exc.errors(), # 예외 객체 에러를 응답 본문으로 전달
    )
# @app.get("/")
# def hello():
#     return {"Hello":"FastAPI"}