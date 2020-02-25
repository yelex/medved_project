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
    product_images = ProductImage.objects.filter(is_active=True, is_main=True)
    return render(request, 'landing/home.html', context=locals())