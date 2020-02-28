from django.shortcuts import render
from landing.forms import SubscriberForm
from products.models import ProductImage

# Create your views here.
def landing(request):
    name = 'CodingMedved'
    form = SubscriberForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        # print(request.POST)
        data = form.cleaned_data
        print(data['name'])
        form.save()
        
    return render(request, 'landing/landing.html', context=locals())

def home(request):
    product_images = ProductImage.objects.filter(is_active=True, is_main=True, product__is_active=True)
    product_images_photos = product_images.filter(product__category__name='phones')
    product_images_laptops = product_images.filter(product__category__name='laptops')
    return render(request, 'landing/home.html', context=locals())