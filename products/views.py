from django.shortcuts import render
from landing.forms import SubscriberForm
from products.models import *

# Create your views here.

def product(request, product_id):    
    product = Product.objects.get(id=product_id)
    return render(request, 'products/product.html', context=locals())

