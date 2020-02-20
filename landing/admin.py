from django.contrib import admin
from landing.models import Subscriber

class SubscriberAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Subscriber._meta.fields]

    class Meta:
        model = Subscriber

admin.site.register(Subscriber, SubscriberAdmin)