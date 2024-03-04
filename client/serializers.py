from django.contrib.auth.models import User
from rest_framework import serializers

from client.models import Client


class ClientSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    email = serializers.CharField(source='user.email')
    username = serializers.CharField(source='user.username')
    last_login = serializers.CharField(source='user.last_login')
    date_joined = serializers.CharField(source='user.date_joined')

    class Meta:
        model = Client
        fields = ('id', 'phone', 'username', 'last_login', 'date_joined', 'email')