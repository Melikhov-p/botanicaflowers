from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client', verbose_name='Пользователь')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{11}$', message="Формат телефонного номер должен быть +79999999999")
    phone = models.CharField(validators=[phone_regex], max_length=17, unique=True, db_index=True, verbose_name='Телефон')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.user.username

