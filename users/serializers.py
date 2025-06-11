# notelog-api/users/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['name'] = self.user.name  # nameをフロントへ返す
        return data

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password')

    def create(self, validated_data):
        return User.objects.create_user(
            name=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password']
        )

class CustomRegisterSerializer(RegisterSerializer):
    """dj-rest-auth用のカスタム登録シリアライザー（usernameなし）"""
    username = None  # usernameフィールドを削除
    name = serializers.CharField(required=True, max_length=150)
    
    def get_cleaned_data(self):
        return {
            'name': self.validated_data.get('name', ''),
            'email': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
        }
    
    def save(self, request):
        cleaned_data = self.get_cleaned_data()
        user = User.objects.create_user(
            name=cleaned_data['name'],
            email=cleaned_data['email'],
            password=cleaned_data['password1']
        )
        return user