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
    likes_count = serializers.SerializerMethodField()

    def get_total_price(self, instance: Product):
        return instance.price - (instance.price * instance.discount_percent / 100)

    def get_likes_count(self, instance: Product):
        return instance.likes.count()

    class Meta:
        model = Product
        fields = ('id', 'category', 'name', 'image',  'price',  'discount_percent', 'total_price', 'description', 'amount', 'available', 'likes_count')


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('product', )
