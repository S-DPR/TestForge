import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth.settings')
django.setup()

import grpc
from django.core.exceptions import ObjectDoesNotExist
from concurrent import futures
from auth import v1_pb2, v1_pb2_grpc
from db.account import service as account_service
from authentication.auth_service import authenticate_user, get_tokens_for_user

class AuthenticateServicer(v1_pb2_grpc.AuthenticateServicer):
    def __init__(self):
        self.LoginReq = getattr(v1_pb2, 'LoginReq', None)
        self.LoginRes = getattr(v1_pb2, 'LoginRes', None)
        self.RefreshReq = getattr(v1_pb2, 'RefreshReq', None)
        self.RefreshRes = getattr(v1_pb2, 'RefreshRes', None)

    def Login(self, request, context):
        try:
            user = authenticate_user(request.username, request.password)
            tokens = get_tokens_for_user(user)
            return self.LoginRes(access=tokens['access'], refresh=tokens['refresh'])
        except Exception as e:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, str(e))

    def Refresh(self, request, context):
        try:
            refresh_token = request.refresh
            refresh = RefreshToken(refresh_token)
            access = str(refresh.access_token)
            return self.RefreshRes(access=access)
        except Exception:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid refresh token")


class AccountServiceServicer(v1_pb2_grpc.AccountServiceServicer):
    def __init__(self):
        self.AccountCreateReq = getattr(v1_pb2, 'AccountCreateReq', None)
        self.AccountGetReq = getattr(v1_pb2, 'AccountGetReq', None)
        self.AccountUpdateReq = getattr(v1_pb2, 'AccountUpdateReq', None)
        self.AccountDeleteReq = getattr(v1_pb2, 'AccountDeleteReq', None)
        self.AccountRes = getattr(v1_pb2, 'AccountRes', None)
        self.AccountDelRes = getattr(v1_pb2, 'AccountDelRes', None)

    def CreateAccount(self, request, context):
        account = account_service.create_account(request.login_id, request.password)
        return self.AccountRes(id=account.id, login_id=account.login_id, password=account.password)

    def GetAccount(self, request, context):
        try:
            account = account_service.get_account(request.account_id)
            return self.AccountRes(id=account.id, login_id=account.login_id, password=account.password)
        except ObjectDoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Account not found")

    def UpdateAccount(self, request, context):
        try:
            account = account_service.update_account(request.account_id, request.login_id, request.password)
            return self.AccountRes(id=account.id, login_id=account.login_id, password=account.password)
        except ObjectDoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Account not found")

    def DeleteAccount(self, request, context):
        try:
            account_service.delete_account(request.account_id)
            return self.AccountDelRes(success=True)
        except ObjectDoesNotExist:
            return self.AccountDelRes(success=False)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    v1_pb2_grpc.add_AccountServiceServicer_to_server(AccountServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Authentication 서버 실행")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
