from django.shortcuts import render
from landing.forms import SubscriberForm
from products.models import ProductImage

# Create your views here.
from django.core.mail import send_mail

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
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()
    # print(session_key)
    product_images = ProductImage.objects.filter(is_active=True, is_main=True, product__is_active=True)
    return render(request, 'landing/home.html', context=locals())


def boucket(request):
    product_images = ProductImage.objects.filter(is_active=True, is_main=True, product__is_active=True,
                                                 product__category__name='букеты')
    return render(request, 'landing/boucket.html', context=locals())


def flower_basket(request):
    product_images = ProductImage.objects.filter(is_active=True, is_main=True, product__is_active=True,
                                                 product__category__name='корзины')
    return render(request, 'landing/flowers_basket.html', context=locals())


def flower_box(request):
    product_images = ProductImage.objects.filter(is_active=True, is_main=True, product__is_active=True,
                                                 product__category__name='коробки')
    return render(request, 'landing/flowers_box.html', context=locals())

def delivery(request):
    return render(request, 'landing/delivery.html')

