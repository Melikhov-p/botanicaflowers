from django.conf import settings
from django.db import models
from django.urls import reverse
from .tasks import set_product_discount_by_category
from client.models import Client


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    image = models.ImageField(upload_to='categories', verbose_name='Изображение', blank=True, null=True)
    slug = models.SlugField(unique=True, verbose_name='URL', blank=True)
    discount_percent = models.IntegerField(default=0, verbose_name='Процент скидки')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__discount_percent = self.discount_percent

    def save(self, *args, **kwargs):
        if self.discount_percent != self.__discount_percent:
            for product in self.products.all():
                set_product_discount_by_category.delay(product.id)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('goods:product_list_by_category', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField(max_length=255, verbose_name='Название')
    image = models.ImageField(upload_to='products', verbose_name='Изображение', blank=True, null=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    price = models.PositiveIntegerField(default=0, verbose_name='Цена')
    available = models.BooleanField(default=True, verbose_name='В наличии')
    amount = models.PositiveIntegerField(default=1, verbose_name='Количество')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    discount_percent = models.IntegerField(default=0, verbose_name='Процент скидки')

    class Meta:
        ordering = ('name', 'price')
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def get_absolute_url(self):
        return reverse('goods:product', args=[self.id, self.slug])

    def __str__(self):
        return self.name


class Like(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Пользователь", null=True, blank=True, related_name='likes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт", related_name='likes')

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = "Лайки"

    def __str__(self):
        return f"{self.product} - {self.client.user.username}"
