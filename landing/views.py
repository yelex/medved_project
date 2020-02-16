from django.shortcuts import render
from landing.forms import SubscriberForm

# Create your views here.
def landing(request):
    name = 'CodingMedved'
    form = SubscriberForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        # print(request.POST)
        data = form.cleaned_data
        print(data['name'])
        form.save()
        
    return render(request, 'landing.html', context=locals())