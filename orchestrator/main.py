from fastapi import FastAPI
import service.code_service as code_service

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

from pydantic import BaseModel

class RunRequest(BaseModel):
    format_: dict
    code1: str
    code2: str
    time_limit: int
    repeat_count: int

@app.post("/runnn")
async def runnn(request: RunRequest):
    return await code_service.run(
        request.format_,
        request.code1,
        request.code2,
        request.time_limit,
        request.repeat_count
    )
