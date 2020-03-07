from django.db import models
from products.models import Product
from django.db.models import signals
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
    total_order_price = models.DecimalField(max_digits=15, decimal_places=2, default=0) # total price for all products in Order
    customer_email = models.EmailField(blank=True, null=True)
    customer_name = models.CharField(max_length=128)
    customer_phone = models.CharField(max_length=48, blank=True, null=True)
    customer_address = models.CharField(max_length=128, blank=True, null=True, default="Укажите адрес доставки")
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    comments = models.TextField(blank=True, null=True, default=None)

    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "Заказ %s статус - %s" % (self.id, self.status.name)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


    def save(self, *args, **kwargs):
        
        super(Order, self).save(*args, **kwargs)


class ProductInOrder(models.Model):
    order = models.ForeignKey(to=Order, blank=True, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, blank=True, null=True, on_delete=models.CASCADE)
    nmb = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=15, decimal_places=2, default=0) # price_per_item * nmb
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "Товар %s в заказе №%s" % (self.product.name, self.order.id)

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def save(self, *args, **kwargs):
        price_per_item = self.product.price
        self.price_per_item = price_per_item

        self.total_price = int(self.nmb) * price_per_item

        super(ProductInOrder, self).save(*args, **kwargs)

def product_in_order_post_save(sender, instance, created, **kwargs):

    order = instance.order
    all_products_in_order = ProductInOrder.objects.filter(order=order, is_active=True)

    order_total_price = 0
    for item in all_products_in_order:
        order_total_price += item.total_price

    instance.order.total_order_price = order_total_price
    instance.order.save(force_update=True)
    

signals.post_save.connect(product_in_order_post_save, sender=ProductInOrder)


class ProductInBasket(models.Model):
    session_key = models.CharField(max_length=128, blank=True, null=True, default=None)
    order = models.ForeignKey(to=Order, blank=True, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, blank=True, null=True, on_delete=models.CASCADE)
    nmb = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)  # price_per_item * nmb
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.product.name

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def save(self, *args, **kwargs):
        price_per_item = self.product.price
        self.price_per_item = price_per_item

        self.total_price = int(self.nmb) * price_per_item

        super(ProductInBasket, self).save(*args, **kwargs)