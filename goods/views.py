from django.conf import settings
from django.db.models import Prefetch, F, Sum
from django.shortcuts import render
from rest_framework import status, filters
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from django.core.cache import cache

from client.models import Client
from goods.models import Product, Category, Like
from goods.permissions import IsAuthenticatedOrSuperUser
from goods.serializers import ProductSerializer, CategorySerializer, LikeSerializer


def index(request):
    return render(request, 'main_app.html')


class CategoryView(ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Category.objects.all().order_by('id')
        return queryset


class ProductView(ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'category__name']
    ordering_fields = ['price', 'name', 'created_at', 'discount_percent']

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        if product_id:
            queryset = Product.objects.get(id=product_id)
        else:
            queryset = Product.objects.all().select_related('category').order_by('-id')
        available = self.request.query_params.get('available')
        category = self.request.query_params.get('category')
        if available:
            queryset = queryset.filter(available=available)
        if category:
            queryset = queryset.filter(category__slug=category)
        return queryset


class LikeView(ModelViewSet):
    permission_classes = [IsAuthenticatedOrSuperUser]
    authentication_classes = [TokenAuthentication]
    serializer_class = LikeSerializer

    def get_queryset(self):
        client_id = self.request.user.client.id
        queryset = Like.objects.filter(client=client_id)
        return queryset

    def create(self, request, *args, **kwargs):
        product_id = self.request.data.get('product')
        if product_id:
            product = Product.objects.get(id=product_id)
            client = Client.objects.get(id=request.user.client.id)
            like = Like.objects.filter(product=product, client=client).first()
            if like:
                is_like = like.delete()
                return Response(status=status.HTTP_204_NO_CONTENT, data={'like': False})
            else:
                is_like = Like.objects.create(product=product, client=client)
                return Response(status=status.HTTP_201_CREATED, data={'like': True})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': self.request.data})