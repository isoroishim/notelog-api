# notelog-api/notes/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoteViewSet

router = DefaultRouter()
router.register(r'notes', NoteViewSet)  # → /api/notes/ に対応

urlpatterns = router.urls  # ✅ routerのURLだけを返す
