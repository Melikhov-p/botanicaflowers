from django.db import models


class Chat(models.Model):
    start_time = models.DateTimeField(auto_now_add=True, verbose_name='Начат')
    client = models.ForeignKey('client.Client', on_delete=models.CASCADE, verbose_name='Клиент')
    closed = models.BooleanField(default=False, verbose_name='Закрыт')

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'

    def __str__(self):
        return str(self.id)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, verbose_name='Чат')
    sender = models.ForeignKey('client.Client', on_delete=models.CASCADE, verbose_name='Отправитель')
    text = models.TextField(verbose_name='Текст')
    sended_at = models.DateTimeField(auto_now_add=True, verbose_name='Отправлено')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
