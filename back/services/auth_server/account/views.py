from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .auth_service import authenticate_user, get_tokens_for_user
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny
#
#
# class LoginView(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')
#
#         if not email or not password:
#             return Response({'detail': '이메일과 비밀번호를 입력하세요.'}, status=status.HTTP_400_BAD_REQUEST)
#
#         user = authenticate_user(email, password)
#         tokens = get_tokens_for_user(user)
#         response = JsonResponse({"message": "login success"})
#         response.set_cookie(
#             key='access_token',
#             value=tokens['access'],
#             httponly=True,
#             samesite='Lax',
#             path='/',
#             max_age=300
#         )
#         response.set_cookie(
#             key='refresh_token',
#             value=tokens['refresh'],
#             httponly=True,
#             secure=True,
#             samesite='Strict',
#             max_age=3600,
#         )
#         return response
#
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'email': user.email}, status=201)
        return Response(serializer.errors, status=400)

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class CookieTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        access = serializer.validated_data["access"]
        refresh = serializer.validated_data["refresh"]
        user = serializer.user

        res = Response({
            "access": access,
            "user": {
                "id": user.id,
                "email": user.email,
            }
        })

        res.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            # secure=True,
            samesite="Strict",
            max_age=7 * 24 * 60 * 60
        )

        return res

class CookieTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response({"error": "refresh token missing"}, status=401)

        serializer = self.get_serializer(data={"refresh": refresh_token})
        serializer.is_valid(raise_exception=True)

        access = serializer.validated_data["access"]
        refresh = serializer.validated_data.get("refresh")

        res = Response({"access": access})

        if refresh:
            res.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                # secure=True,
                samesite="Strict",
                max_age=7 * 24 * 60 * 60
            )

        return res

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response({"error": "no refresh token"}, status=400)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response({"error": "invalid or expired refresh token"}, status=400)

        res = Response({"message": "logged out"})
        res.delete_cookie("refresh_token")
        return res
