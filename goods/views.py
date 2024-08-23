import base64
import datetime
import io
from django.shortcuts import render
from rest_framework import status, filters
from rest_framework.authentication import  TokenAuthentication
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from client.models import Client
from goods.models import Product, Category, Like
from goods.permissions import IsAuthenticatedOrSuperUser
from goods.serializers import ProductSerializer, CategorySerializer, LikeSerializer


def index(request):
    return render(request, 'main_app.html')


class CategoryView(ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Category.objects.all().order_by('id')
        return queryset


class ProductView(ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'category__name']
    ordering_fields = ['price', 'name', 'created_at', 'discount_percent']
    parser_class = [MultiPartParser, JSONParser]

    def get_queryset(self):
        queryset = Product.objects.all().select_related('category').order_by('-id')
        available = self.request.query_params.get('available')
        category = self.request.query_params.get('category')
        if available:
            queryset = queryset.filter(available=available)
        if category:
            queryset = queryset.filter(category__slug=category)
        return queryset

    def get_object(self):
        product_id = self.kwargs.get('pk')
        product = Product.objects.get(pk=product_id)
        return product

    def create(self, request, *args, **kwargs):
        try:
            if not request.user.is_staff:
                return Response({'detail': 'Недостаточно прав'}, status=status.HTTP_403_FORBIDDEN)
            product_image_base64 = request.data.get('image')
            request.data.pop('image')
            product = Product.objects.create(
                name=request.data.get('name'),
                price=request.data.get('price'),
                discount_percent=request.data.get('discount_percent'),
                amount=request.data.get('amount'),
                available=request.data.get('available'),
                description=request.data.get('description'),
                category_id=request.data.get('category'),
            )
            if product_image_base64:
                image_name = f'{product.category.name.replace(" ", "_")}_{product.name.replace(" ", "_")}_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.jpg'
                image_data = base64.b64decode(product_image_base64.split(',')[1])
                image_bytes = io.BytesIO(image_data)
                product.image.save(image_name, image_bytes)
            product.save()
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        product = self.get_object()
        try:
            if not request.user.is_staff:
                return Response({'detail': 'Недостаточно прав'}, status=status.HTTP_403_FORBIDDEN)
            image = request.data.get('image')
            if image:
                request.data._mutable = True
                image_name = f'{product.category.name.replace(" ", "_")}_{product.name.replace(" ", "_")}_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.jpg'
                image_data = base64.b64decode(image.split(',')[1])
                image_bytes = io.BytesIO(image_data)
                product.image.save(image_name, image_bytes)
                product.save()
                request.data.pop('image')
            product.name = request.data.get('name', product.name)
            product.price = request.data.get('price', product.price)
            product.discount_percent = request.data.get('discount_percent', product.discount_percent)
            product.amount = request.data.get('amount', product.amount)
            if request.data.get('available'):
                if request.data.get('available') == 'true':
                    product.available = True
                else:
                    product.available = False
            else:
                product.available = False
            if request.data.get('category[id]'):
                product.category = Category.objects.get(id=request.data.get('category[id]'))
            product.description = request.data.get('description', product.description)
            product.save()
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


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