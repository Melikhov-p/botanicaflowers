from django.conf import settings
from django.contrib.auth.models import User, update_last_login
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Prefetch, F, Sum
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from django.core.cache import cache
from client.models import Client
from client.permissions import IsAuthenticatedAndOwner
from client.serializers import ClientSerializer, UserLoginSerializer


class ClientView(ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticatedAndOwner]
    lookup_field = 'id'  # поле для поиска через url api/clients/<int:client_id>/

    def create(self, request, *args, **kwargs):
        client_data = self.request.data
        user = User.objects.create_user(username=client_data['phone'], password=client_data['password'])
        client = Client.objects.create(user=user, phone=client_data['phone'])
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'client': client.id}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        user = User.objects.get(id=self.kwargs.get('id'))
        if user != request.user or not request.user.is_staff:
            return Response({'detail': 'Недостаточно прав'}, status=status.HTTP_403_FORBIDDEN)
        client = user.client
        new_data = self.request.data
        if 'phone' in new_data:
            user.username = new_data['phone']
            client.phone = new_data['phone']
            new_data.pop('phone')
        if 'password' in new_data:
            user.set_password(new_data['password'])
            new_data.pop('password')
        if 'email' in new_data:
            user.email = new_data['email']
            new_data.pop('email')
        if 'address' in new_data:
            client.address = new_data['address']
            new_data.pop('address')
        user.save()
        client.save()
        return Response(status=status.HTTP_200_OK)

    def get_queryset(self):
        client_id = self.kwargs.get('client_id')
        if client_id:
            queryset = Client.objects.get(id=client_id)
        else:
            queryset = Client.objects.all().select_related('user').order_by('id')
        return queryset


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.filter(username=request.data['username']).first()
        if user:
            if user.check_password(request.data['password']):
                token = Token.objects.get(user=user)
                update_last_login(None, user)
                return Response({'token': token.key, 'client': user.client.id}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

