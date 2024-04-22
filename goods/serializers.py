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

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.category = validated_data.get('category', instance.category)
        instance.price = validated_data.get('price', instance.price)
        instance.discount_percent = validated_data.get('discount_percent', instance.discount_percent)
        instance.description = validated_data.get('description', instance.description)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.available = validated_data.get('available', instance.available)
        instance.save()
        return instance

    class Meta:
        model = Product
        fields = ('id', 'category', 'name', 'image',  'price',  'discount_percent', 'total_price', 'description', 'amount', 'available', 'likes_count')


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('product', )
