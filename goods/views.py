from django.conf import settings
from django.db.models import Prefetch, F, Sum
from django.shortcuts import render
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.core.cache import cache

from goods.models import Product, Category, Like
from goods.serializers import ProductSerializer, CategorySerializer, LikeSerializer


class CategoryView(ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Category.objects.all().order_by('id')
        return queryset


class ProductView(ReadOnlyModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        if product_id:
            queryset = Product.objects.get(id=product_id)
        else:
            queryset = Product.objects.all().select_related('category').order_by('id')
        available = self.request.query_params.get('available')
        category = self.request.query_params.get('category')
        if available:
            queryset = queryset.filter(available=available)
        if category:
            queryset = queryset.filter(category__slug=category)
        return queryset



class LikeView(ReadOnlyModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = LikeSerializer

    def get_queryset(self):
        queryset = Like.objects.all().prefetch_related(
            'client',
            Prefetch('product', queryset=Product.objects.select_related('category'))
        ).order_by('id')
        return queryset

