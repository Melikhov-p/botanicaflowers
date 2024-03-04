# импортируем из созданного нами ранее файла celery_app.py наш объект(экземпляр класса) celery (app)
from celery_app import app as celery_app
# Подключаем объект
__all__ = ('celery_app',)