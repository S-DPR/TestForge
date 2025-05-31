from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def authenticate_user(login_id, password):
    user = authenticate(login_id=login_id, password=password)
    if user is None or not user.is_active:
        raise AuthenticationFailed("Invalid login_id or password.")
    return user