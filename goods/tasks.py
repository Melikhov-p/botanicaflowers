from celery import shared_task
from django.db import transaction
from celery_singleton import Singleton


@shared_task(base=Singleton)
def set_product_discount_by_category(product_id):
    from goods.models import Product
    with transaction.atomic():
        product = Product.objects.select_for_update().get(id=product_id)
        product.discount_percent = product.category.discount_percent
        product.save()
