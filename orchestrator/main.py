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

@app.post("/testforge")
async def testforge(request: RunRequest):
    return await code_service.code_service.queue_push(
        request.format_,
        request.code1,
        request.code2,
        request.time_limit,
        request.repeat_count
    )

###########################################
# GPT 사용, 테스트용 엔드포인트
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from auth import client  # client.py 니가 만든 거 import

app = FastAPI(title="gRPC Auth Test API")

# -------------------
# 요청/응답 스키마 정의
# -------------------

class LoginRequest(BaseModel):
    username: str
    password: str

class RefreshRequest(BaseModel):
    refresh: str

class AccountCreateRequest(BaseModel):
    login_id: str
    password: str

class AccountUpdateRequest(BaseModel):
    account_id: str
    login_id: str
    password: str

class AccountGetDeleteRequest(BaseModel):
    account_id: str

# -------------------
# 엔드포인트 정의
# -------------------

@app.post("/login")
def login(req: LoginRequest):
    res = client.login(req.username, req.password)
    if res is None:
        raise HTTPException(status_code=401, detail="Login failed")
    return res

@app.post("/refresh")
def refresh(req: RefreshRequest):
    res = client.refresh(req.refresh)
    if res is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    return res

@app.post("/account")
def create_account(req: AccountCreateRequest):
    res = client.create_account(req.login_id, req.password)
    if res is None:
        raise HTTPException(status_code=400, detail="Account creation failed")
    return res

@app.get("/account/{account_id}")
def get_account(account_id: str):
    res = client.get_account(account_id)
    if res is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return res

@app.put("/account")
def update_account(req: AccountUpdateRequest):
    res = client.update_account(req.account_id, req.login_id, req.password)
    if res is None:
        raise HTTPException(status_code=400, detail="Update failed")
    return res

@app.delete("/account/{account_id}")
def delete_account(account_id: str):
    res = client.delete_account(account_id)
    if res is None:
        raise HTTPException(status_code=400, detail="Delete failed")
    return res