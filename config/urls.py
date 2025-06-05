# notelog-api/config/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT 認証（ログイン・リフレッシュ）
    path('api/auth/', include('users.urls')),  # users/urls.py で login/ や refresh/ を定義

    # Note CRUD API
    path('api/', include('notes.urls')),       # notes/urls.py で router 経由で登録
]
