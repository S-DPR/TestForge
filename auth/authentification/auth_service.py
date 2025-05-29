from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def authenticate_user(username, password):
    user = authenticate(username=username, password=password)
    if user is None:
        raise Exception("Invalid credentials")
    return user
