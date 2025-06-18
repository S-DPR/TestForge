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

# @app.post("/testforge")
# async def testforge(request: RunRequest):
#     return await code_service.code_service.queue_push(
#         request.format_,
#         request.code1,
#         request.code2,
#         request.time_limit,
#         request.repeat_count
#     )


from auth import client
from fastapi import FastAPI, HTTPException

class AuthRequest(BaseModel):
    login_id: str
    password: str

class RefreshRequest(BaseModel):
    refresh: str

@app.post("/login")
def login(data: AuthRequest):
    result = client.login(username=data.login_id, password=data.password)
    if not result:
        raise HTTPException(status_code=401, detail="Login failed.")
    return result

@app.post("/register")
def register(data: AuthRequest):
    result = client.register(login_id=data.login_id, password=data.password)
    if not result:
        raise HTTPException(status_code=409, detail="Registration failed.")
    return result

@app.post("/refresh")
def refresh_token(data: RefreshRequest):
    result = client.refresh(refresh_token=data.refresh)
    if not result:
        raise HTTPException(status_code=401, detail="Token refresh failed.")
    return result

@app.post("/inactive")
def deactivate(data: AuthRequest):
    result = client.deactivate(login_id=data.login_id, password=data.password)
    if not result:
        raise HTTPException(status_code=500, detail="Deactivation failed.")
    return result