from django import forms
from landing.models import Subscriber

class SubscriberForm(forms.ModelForm):

    class Meta:
        model = Subscriber
        exclude = [""]