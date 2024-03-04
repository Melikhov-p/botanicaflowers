from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.response import Response

from client.models import Client
from goods.models import Like


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
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        client = Client.objects.create(user=user, **validated_data)
        return client

    class Meta:
        model = Client
        fields = ('id', 'phone', 'username', 'first_name', 'last_name', 'last_login', 'date_joined', 'email', 'likes', 'password')
