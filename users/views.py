from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.http import JsonResponse
from django.urls import reverse
from allauth.socialaccount.models import SocialApp, SocialAccount
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomTokenObtainPairSerializer, UserRegisterSerializer

User = get_user_model()

# JWTログインビュー（トークン＋username返却）
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# ユーザー登録ビュー
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

# Google OAuth2 ログイン（django-allauth使用）
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://127.0.0.1:8000/api/auth/google/callback/"
    client_class = OAuth2Client

# Googleログインリダイレクト
def google_login(request):
    """django-allauthのGoogle認証へリダイレクト"""
    # allauth標準のGoogle認証URLを使用
    return redirect('/accounts/google/login/')

# Googleコールバック処理
def google_callback(request):
    """Google認証コールバック処理"""
    # エラーチェック
    error = request.GET.get('error')
    if error:
        return JsonResponse({'error': error}, status=400)
    
    code = request.GET.get('code')
    if not code:
        return JsonResponse({'error': 'Authorization code not found'}, status=400)
    
    try:
        # allauth経由でユーザー情報を取得
        from allauth.socialaccount.helpers import complete_social_login
        from allauth.socialaccount.models import SocialLogin
        from allauth.socialaccount.providers.google.provider import GoogleProvider
        
        # ここでallauthの処理を利用
        # 実際の処理はallauthのcallbackビューで行われるため、
        # フロントエンドへのリダイレクトのみ行う
        
        # 一時的にセッションに保存
        request.session['google_auth_code'] = code
        
        # フロントエンドにリダイレクト
        frontend_url = "http://localhost:5173/auth/callback?provider=google"
        return redirect(frontend_url)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Google認証後のトークン取得API
class GoogleAuthTokenView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Google認証後、JWTトークンを発行"""
        email = request.data.get('email')
        
        if not email:
            return Response(
                {'error': 'Email is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Googleでログインしたユーザーを確認
            user = User.objects.get(email=email)
            
            # ソーシャルアカウントの確認
            social_account = SocialAccount.objects.filter(
                user=user,
                provider='google'
            ).first()
            
            if not social_account:
                return Response(
                    {'error': 'User not authenticated with Google'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # JWTトークンを生成
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'email': user.email,
                    'name': user.name,
                }
            })
            
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )