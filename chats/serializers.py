from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.response import Response

from chats.models import Chat, Message
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ('id', 'client', 'start_time')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'chat', 'sender', 'text', 'sended_at')
