from django.shortcuts import render
from landing.forms import SubscriberForm
from products.models import *

# Create your views here.


def product(request, product_id):    
    product = Product.objects.get(id=product_id)
    main_image = ProductImage.objects.filter(product=product, is_main=True)[0]

    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    print(session_key)

    return render(request, 'products/product.html', context=locals())

