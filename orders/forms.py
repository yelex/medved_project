from django import forms


class CheckoutContactForm(forms.Form):
    name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    note = forms.CharField()
    is_delivery = forms.BooleanField()
    is_other_person = forms.BooleanField()
    name_other = forms.CharField()
    phone_other = forms.CharField()
    delivery_address = forms.CharField()
    delivery_date = forms.DateField(required=True)
    comments = forms.CharField()


