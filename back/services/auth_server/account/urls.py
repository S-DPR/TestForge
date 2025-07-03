from django.urls import path
from .views import CookieTokenObtainPairView, CookieTokenRefreshView, LogoutView, RegisterView
# from .view import LoginView, RegisterView

urlpatterns = [
    # path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    # path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('logout/', LogoutView.as_view(), name='logout'),

    path('login/', CookieTokenObtainPairView.as_view(), name='login'),
    path('refresh/', CookieTokenRefreshView.as_view(), name='refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
]