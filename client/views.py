from django.conf import settings
from django.db.models import Prefetch, F, Sum
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.core.cache import cache
from client.models import Client
from client.serializers import ClientSerializer


class ClientView(ReadOnlyModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        client_id = self.kwargs.get('client_id')
        if client_id:
            queryset = Client.objects.get(id=client_id)
        else:
            queryset = Client.objects.all().select_related('user').order_by('id')
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response_data = {
            'status': 'ok',
            'data': response.data,
        }
        response.data = response_data
        return response
