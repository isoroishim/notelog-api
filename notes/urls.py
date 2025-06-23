# notelog-api/notes/urls.py
from django.urls import path
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def note_list_placeholder(request):
    """ノート一覧API（プレースホルダー）"""
    return Response({'message': 'ノート機能は開発中です', 'notes': []})

@api_view(['POST'])
def note_create_placeholder(request):
    """ノート作成API（プレースホルダー）"""
    return Response({'message': 'ノート作成機能は開発中です'})

urlpatterns = [
    # ノート関連API（プレースホルダー）
    path('', note_list_placeholder, name='note_list'),
    path('create/', note_create_placeholder, name='note_create'),
]