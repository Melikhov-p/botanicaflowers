from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Prefetch, F, Sum
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from django.core.cache import cache
from client.models import Client
from client.permissions import IsAuthenticatedAndOwner
from client.serializers import ClientSerializer, UserLoginSerializer
from client.utils import get_and_authenticate_user


class ClientView(ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticatedAndOwner]
    lookup_field = 'id'  # поле для поиска через url api/clients/<int:client_id>/

    def create(self, request, *args, **kwargs):
        client_data = self.request.data
        user = User.objects.create_user(username=client_data['phone'], password=client_data['password'], first_name=client_data.get('first_name'), last_name=client_data.get('last_name'))
        client = Client.objects.create(user=user, phone=client_data['phone'])
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'client': client.id}, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        client_id = self.kwargs.get('client_id')
        if client_id:
            queryset = Client.objects.get(id=client_id)
        else:
            queryset = Client.objects.all().select_related('user').order_by('id')
        return queryset


class AuthViewSet(viewsets.GenericViewSet):
    serializer_class = UserLoginSerializer

