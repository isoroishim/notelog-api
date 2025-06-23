from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CustomTokenObtainPairView, 
    UserRegisterView, 
    GoogleLogin,
    GoogleAuthTokenView,
    google_login,
    google_callback
)

urlpatterns = [
    # JWT 認証エンドポイント
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserRegisterView.as_view(), name="user_register"),

    # Google OAuth2 ログイン
    path("google/", google_login, name="google_login"),
    path("google/callback/", google_callback, name="google_callback"),
    path("google/token/", GoogleAuthTokenView.as_view(), name="google_token"),
    
    # dj-rest-auth Google認証（API用）
    path("google/login/", GoogleLogin.as_view(), name="google_api_login"),
]