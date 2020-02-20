from django.db import models
from products.models import Product
# Create your models here.

class Status(models.Model):
    name = models.CharField(max_length=24)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "Статус %s" % self.name

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Order(models.Model):
    total_order_price = models.DecimalField(max_digits=15, decimal_places=2) # total price for all products in Order
    customer_email = models.EmailField(blank=True, null=True, default="Укажите e-mail")
    customer_name = models.CharField(max_length=128, default="Укажите имя")
    customer_phone = models.CharField(max_length=48, blank=True, null=True, default="Укажите номер телефона")
    customer_address = models.CharField(max_length=128, blank=True, null=True, default="Укажите адрес доставки")
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    comments = models.TextField(blank=True, null=True, default=True)

    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "Заказ %s статус - %s" % (self.id, self.status.name)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class ProductInOrder(models.Model):
    order = models.ForeignKey(to=Order, blank=True, null=True, default=True, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, blank=True, null=True, default=True, on_delete=models.CASCADE)
    nmb = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=15, decimal_places=2) # price_per_item * nmb
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "Товар %s в заказе №%s" % (self.product.name, self.order.id)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

