# notelog-api/config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django管理画面
    path('admin/', admin.site.urls),
    
    # allauth標準URL（セッションベース認証用）
    path('accounts/', include('allauth.urls')),
    
    # カスタムAPI（優先度高）
    path('api/auth/', include('users.urls')),
    path('api/notes/', include('notes.urls')),
    
    # dj-rest-auth API（標準）
    path('api/dj-rest-auth/', include('dj_rest_auth.urls')),
    path('api/dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    
    # フロントエンド用の短縮パス
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
]

# 開発環境でのメディアファイル配信
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# デバッグ用：URL一覧を表示
if settings.DEBUG:
    import logging
    logger = logging.getLogger(__name__)
    logger.info("=== URL Configuration ===")
    logger.info("API endpoints:")
    logger.info("  /api/auth/google/token/ (POST)")
    logger.info("  /api/auth/login/ (POST)")
    logger.info("  /api/auth/register/ (POST)")
    logger.info("  /dj-rest-auth/google/ (POST)")
    logger.info("=========================")