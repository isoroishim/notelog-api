# notelog-api/users/views.py
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework_simplejwt.tokens import RefreshToken
import requests
import logging

# シリアライザのインポート
from .serializers import CustomTokenObtainPairSerializer, UserRegisterSerializer

User = get_user_model()
logger = logging.getLogger(__name__)

# JWTログインビュー
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# ユーザー登録ビュー
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

# Google認証トークン生成ビュー（メインAPI）
@method_decorator(csrf_exempt, name='dispatch')
class GoogleAuthTokenView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        """GET時は簡単な確認メッセージを返す"""
        return Response({
            'message': 'Google Auth Token API endpoint is working',
            'method': 'POST required with code parameter'
        })
    
    def post(self, request):
        """Googleの認証コードからJWTトークンを発行"""
        try:
            code = request.data.get('code')
            logger.info(f"Google auth request received. Code: {code[:10] if code else 'None'}...")
            
            if not code:
                return Response(
                    {'error': 'Authorization code is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Google OAuth2設定を取得
            try:
                client_id = settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id']
                client_secret = settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['secret']
            except (AttributeError, KeyError):
                # 設定が見つからない場合は環境変数から取得
                client_id = getattr(settings, 'GOOGLE_OAUTH2_CLIENT_ID', None)
                client_secret = getattr(settings, 'GOOGLE_OAUTH2_CLIENT_SECRET', None)
            
            if not client_id or not client_secret:
                logger.error("Google OAuth2 credentials not found")
                return Response(
                    {'error': 'Google OAuth2 credentials not configured'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            redirect_uri = 'http://localhost:5173/auth/callback'
            
            logger.info(f"Making Google token request with client_id: {client_id[:10]}...")
            
            # Googleからアクセストークンを取得
            token_response = requests.post('https://oauth2.googleapis.com/token', data={
                'client_id': client_id,
                'client_secret': client_secret,
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': redirect_uri,
            }, timeout=10)
            
            logger.info(f"Google token response: {token_response.status_code}")
            
            if token_response.status_code != 200:
                logger.error(f"Google token error: {token_response.text}")
                return Response(
                    {
                        'error': 'Failed to obtain access token from Google',
                        'details': token_response.text,
                        'status_code': token_response.status_code
                    }, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            token_data = token_response.json()
            access_token = token_data.get('access_token')
            
            if not access_token:
                logger.error(f"No access token in Google response: {token_data}")
                return Response(
                    {'error': 'Access token not found in Google response'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            logger.info("Getting user info from Google...")
            
            # Googleからユーザー情報を取得
            user_response = requests.get(
                'https://www.googleapis.com/oauth2/v2/userinfo',
                headers={'Authorization': f'Bearer {access_token}'},
                timeout=10
            )
            
            if user_response.status_code != 200:
                logger.error(f"Google user info error: {user_response.text}")
                return Response(
                    {'error': 'Failed to obtain user info from Google'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user_data = user_response.json()
            email = user_data.get('email')
            name = user_data.get('name', user_data.get('given_name', ''))
            google_id = user_data.get('id', '')
            
            logger.info(f"Google user data: email={email}, name={name}")
            
            if not email:
                return Response(
                    {'error': 'Email not found in Google user data'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # ユーザーを取得または作成
            user, created = User.objects.get_or_create(
                email=email,
                defaults={'name': name if name else email.split('@')[0]}
            )
            
            if created:
                logger.info(f"New user created: {user.email}")
            else:
                logger.info(f"Existing user found: {user.email}")
                # 既存ユーザーの名前を更新（空の場合のみ）
                if not user.name and name:
                    user.name = name
                    user.save()
            
            # JWTトークンを生成
            refresh = RefreshToken.for_user(user)
            
            response_data = {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'name': user.name,
                }
            }
            
            logger.info(f"JWT token generated successfully for user: {user.email}")
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error during Google auth: {str(e)}")
            return Response(
                {'error': f'Network error: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.error(f"Unexpected error during Google auth: {str(e)}", exc_info=True)
            return Response(
                {'error': f'Authentication failed: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# django-allauth用のGoogleログインビュー（バックアップ）
try:
    from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
    from allauth.socialaccount.providers.oauth2.client import OAuth2Client
    from dj_rest_auth.registration.views import SocialLoginView
    
    class GoogleLogin(SocialLoginView):
        adapter_class = GoogleOAuth2Adapter
        callback_url = "http://localhost:8000/api/auth/google/callback/"
        client_class = OAuth2Client
        
        def get_response(self):
            """レスポンス形式をカスタマイズ"""
            if getattr(settings, 'REST_AUTH', {}).get('USE_JWT', False):
                # JWT使用時
                refresh = RefreshToken.for_user(self.user)
                
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': {
                        'pk': self.user.pk,
                        'email': self.user.email,
                        'name': getattr(self.user, 'name', ''),
                    }
                })
            else:
                return super().get_response()

except ImportError as e:
    logger.warning(f"allauth import error: {e}")
    
    class GoogleLogin(APIView):
        permission_classes = [AllowAny]
        
        def post(self, request):
            return Response({'error': 'allauth not properly configured'}, status=500)

# ヘルパービュー
@api_view(['GET'])
@permission_classes([AllowAny])
def google_login(request):
    """Google認証開始エンドポイント"""
    return redirect('/accounts/google/login/')

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@csrf_exempt
def google_callback(request):
    """Google認証コールバック処理"""
    try:
        error = request.GET.get('error')
        if error:
            logger.error(f"Google callback error: {error}")
            return JsonResponse({'error': error}, status=400)
        
        code = request.GET.get('code')
        if not code:
            return JsonResponse({'error': 'Authorization code not found'}, status=400)
        
        # フロントエンドにリダイレクト
        frontend_url = f"http://localhost:5173/auth/callback?code={code}"
        return redirect(frontend_url)
        
    except Exception as e:
        logger.error(f"Google callback error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)