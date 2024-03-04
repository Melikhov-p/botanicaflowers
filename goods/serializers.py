from django.contrib.auth.models import User
from rest_framework import serializers

from goods.models import Category, Product, Like


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'discount_percent', 'slug')


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, instance: Product):
        return instance.price - (instance.price * instance.discount_percent / 100)

    class Meta:
        model = Product
        fields = ('id', 'category', 'name', 'image',  'price',  'discount_percent', 'total_price', 'description', 'amount', 'available')


class LikeSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Like
        fields = ('client', 'product')
