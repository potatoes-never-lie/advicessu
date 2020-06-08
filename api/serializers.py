from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Post

User._meta.get_field('email')._unique=True    ##중복 이메일 체크

# 회원가입
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email",
            "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"], 
            validated_data["email"],
            validated_data["password"]
        )
        #user=User.objects.create_user(**validated_data)
        #user.is_active=True
        return user


# 접속 유지중인지 확인
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


# 로그인
class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")

class PostSerializer(serializers.ModelSerializer):
    author=serializers.ReadOnlyField(source='author.username')
    class Meta:
        model=Post
        fields=("id","title","text","created_date","author")
        # fields=("id","author","title","text","published_date")
        # fields=("author","title","text")
        # fields=("id","title","text")