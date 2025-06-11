from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 管理画面
    path('admin/', admin.site.urls),
    
    # allauth標準URL（セッションベース認証用）
    path('accounts/', include('allauth.urls')),
    
    # REST API
    path('api/auth/', include('users.urls')),
    path('api/notes/', include('notes.urls')),
    
    # dj-rest-auth（JWT認証用）
    path('api/dj-rest-auth/', include('dj_rest_auth.urls')),
    path('api/dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
]

# 開発環境でのメディアファイル配信
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)