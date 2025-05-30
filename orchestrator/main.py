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

# 요청 모델
class AuthRequest(BaseModel):
    login_id: str
    password: str

class RefreshRequest(BaseModel):
    refresh: str

# 로그인
@app.post("/login")
def login(data: AuthRequest):
    try:
        req = v1_pb2.LoginReq(login_id=data.login_id, password=data.password)
        res = auth_stub.Login(req)
        return {"access": res.access, "refresh": res.refresh}
    except grpc.RpcError as e:
        raise HTTPException(status_code=401, detail=f"Login failed: {e.details()}")

# 회원가입
@app.post("/register")
def register(data: AuthRequest):
    try:
        req = v1_pb2.RegisterReq(login_id=data.login_id, password=data.password)
        res = auth_stub.Register(req)
        return {"access": res.access, "refresh": res.refresh}
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.ALREADY_EXISTS:
            raise HTTPException(status_code=409, detail="User already exists.")
        raise HTTPException(status_code=500, detail="Registration failed.")

# 탈퇴 / 비활성화
@app.post("/inactive")
def inactivate(data: AuthRequest):
    try:
        req = v1_pb2.InActiveReq(login_id=data.login_id, password=data.password)
        res = auth_stub.InActive(req)
        return {"message": res.message}
    except grpc.RpcError as e:
        raise HTTPException(status_code=401, detail=f"Inactivation failed: {e.details()}")

# 토큰 리프레시
@app.post("/refresh")
def refresh_token(data: RefreshRequest):
    try:
        req = v1_pb2.RefreshReq(refresh=data.refresh)
        res = auth_stub.Refresh(req)
        return {"access": res.access}
    except grpc.RpcError as e:
        raise HTTPException(status_code=401, detail=f"Refresh failed: {e.details()}")