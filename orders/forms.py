from django import forms

# FIXME прописать ошибки формы
class CheckoutContactForm(forms.Form):
    name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    note = forms.CharField(required=False)
    is_delivery = forms.BooleanField(required=False)
    is_another_person = forms.BooleanField(required=False)
    name_other = forms.CharField(required=False)
    phone_other = forms.CharField(required=False)
    delivery_address = forms.CharField(required=False)
    delivery_date = forms.CharField(required=True)
    comments = forms.CharField(required=False)