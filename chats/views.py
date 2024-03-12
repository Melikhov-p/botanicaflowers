from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from chats.models import Chat, Message
from chats.serializers import ChatSerializer, MessageSerializer
from client.permissions import IsAuthenticatedAndOwner


class ChatView(ModelViewSet):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticatedAndOwner]
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        client = self.request.user.client
        client_chats = Chat.objects.filter(client=client)
        if self.request.user.is_staff:
            pass
        else:
            for chat in client_chats:
                if not chat.closed:
                    return Response({'chat': chat.id, 'message': 'У вас уже есть открытый чат'}, status=status.HTTP_400_BAD_REQUEST)
        data = {
            'client': client,
        }
        chat = Chat.objects.create(**data)
        return Response({'chat': chat.id}, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Chat.objects.all()
        else:
            client = self.request.user.client
            return Chat.objects.filter(client=client)


class MessageView(ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticatedAndOwner]

    def create(self, request, *args, **kwargs):
        chat = Chat.objects.get(id=self.request.data.get('chat_id'))
        sender = self.request.user.client
        message = Message.objects.create(chat=chat, sender=sender, text=self.request.data.get('text'))
        return Response({'message': message.id}, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        chat_id = self.request.data.get('chat_id')
        if chat_id:
            queryset = Message.objects.filter(chat=chat_id).order_by('sended_at')
        else:
            queryset = []
        return queryset
