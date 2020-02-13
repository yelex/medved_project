from django.shortcuts import render
from landing.forms import SubscriberForm

# Create your views here.
def landing(request):
    name = 'CodingMedved'
    form = SubscriberForm(request.POST or None)

    if request.method == 'POST':
        print(form)
        
    return render(request, 'landing/landing.html', context=locals())