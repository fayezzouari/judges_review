from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Judgement



class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [ "username", "password"]


class JudgementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Judgement
        fields = ['id', 'project_id', 'judge']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
