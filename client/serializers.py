from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.response import Response
from client.models import Client
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class ClientSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    email = serializers.CharField(source='user.email')
    username = serializers.CharField(source='user.username')
    password = serializers.CharField(source='user.password')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    last_login = serializers.CharField(source='user.last_login', required=False)
    date_joined = serializers.CharField(source='user.date_joined', required=False)

    def create(self, validated_data):
        print(validated_data)
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        token = Token.objects.create(user=user)
        client = Client.objects.create(user=user, **validated_data)
        client.token = token.key
        return client

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = Client
        fields = ('id', 'phone', 'username', 'first_name', 'last_name', 'last_login', 'date_joined', 'email', 'likes', 'password')


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)

