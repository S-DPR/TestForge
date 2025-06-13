from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .auth_service import authenticate_user, get_tokens_for_user
from .serializers import RegisterSerializer


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'detail': '이메일과 비밀번호를 입력하세요.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate_user(email, password)
        tokens = get_tokens_for_user(user)
        response = JsonResponse({"message": "login success"})
        response.set_cookie(
            key='access_token',
            value=tokens['access'],
            httponly=True,
            samesite='Lax',
            path='/',
            max_age=300
        )
        response.set_cookie(
            key='refresh_token',
            value=tokens['refresh'],
            httponly=True,
            secure=True,
            samesite='Strict',
            max_age=3600,
        )
        return response

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'email': user.email}, status=201)
        return Response(serializer.errors, status=400)
