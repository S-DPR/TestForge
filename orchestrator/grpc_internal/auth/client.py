import grpc
from auth import v1_pb2, v1_pb2_grpc

channel = grpc.insecure_channel("auth:50051")

auth_stub = v1_pb2_grpc.AuthenticateStub(channel)
account_stub = v1_pb2_grpc.AccountServiceStub(channel)

# 로그인 요청
def login(username: str, password: str):
    req = v1_pb2.LoginReq(login_id=username, password=password)
    try:
        res = auth_stub.Login(req)
        return {"access": res.access, "refresh": res.refresh}
    except grpc.RpcError as e:
        print(f"Login failed: {e.code()} {e.details()}")
        return None

# 토큰 리프레시
def refresh(refresh_token: str):
    req = v1_pb2.RefreshReq(refresh=refresh_token)
    try:
        res = auth_stub.Refresh(req)
        return {"access": res.access}
    except grpc.RpcError as e:
        print(f"Refresh failed: {e.code()} {e.details()}")
        return None

# 회원가입
def register(login_id: str, password: str):
    req = v1_pb2.RegisterReq(login_id=login_id, password=password)
    try:
        res = auth_stub.Register(req)
        return {"access": res.access, "refresh": res.refresh}
    except grpc.RpcError as e:
        print(f"Register failed: {e.code()} {e.details()}")
        return None

# 비활성화 (탈퇴)
def deactivate(login_id: str, password: str):
    req = v1_pb2.InActiveReq(login_id=login_id, password=password)
    try:
        res = auth_stub.InActive(req)
        return {"message": res.message}
    except grpc.RpcError as e:
        print(f"Inactive failed: {e.code()} {e.details()}")
        return None

# 계정 생성
def create_account(login_id: str, password: str):
    req = v1_pb2.AccountCreateReq(login_id=login_id, password=password)
    try:
        res = account_stub.CreateAccount(req)
        return {"account_id": res.account_id, "login_id": res.login_id, "password": res.password}
    except grpc.RpcError as e:
        print(f"CreateAccount failed: {e.code()} {e.details()}")
        return None

# 계정 조회
def get_account(account_id: str):
    req = v1_pb2.AccountGetReq(account_id=account_id)
    try:
        res = account_stub.GetAccount(req)
        return {"account_id": res.account_id, "login_id": res.login_id, "password": res.password}
    except grpc.RpcError as e:
        print(f"GetAccount failed: {e.code()} {e.details()}")
        return None

# 계정 수정
def update_account(account_id: str, login_id: str, password: str):
    req = v1_pb2.AccountUpdateReq(account_id=account_id, login_id=login_id, password=password)
    try:
        res = account_stub.UpdateAccount(req)
        return {"account_id": res.account_id, "login_id": res.login_id, "password": res.password}
    except grpc.RpcError as e:
        print(f"UpdateAccount failed: {e.code()} {e.details()}")
        return None

# 계정 삭제
def delete_account(account_id: str):
    req = v1_pb2.AccountDelReq(account_id=account_id)
    try:
        res = account_stub.DeleteAccount(req)
        return {"success": res.success}
    except grpc.RpcError as e:
        print(f"DeleteAccount failed: {e.code()} {e.details()}")
        return None
