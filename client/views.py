from django.conf import settings
from django.db.models import Prefetch, F, Sum
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from django.core.cache import cache
from client.models import Client
from client.permissions import IsAuthenticatedAndOwner
from client.serializers import ClientSerializer


class ClientView(ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticatedAndOwner]
    lookup_field = 'id'  # поле для поиска через url api/clients/<int:client_id>/

    def get_queryset(self):
        client_id = self.kwargs.get('client_id')
        if client_id:
            queryset = Client.objects.get(id=client_id)
        else:
            queryset = Client.objects.all().select_related('user').order_by('id')
        return queryset

