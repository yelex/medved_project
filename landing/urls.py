from django.urls import path, include
from landing import views

urlpatterns = [
    path('', views.home, name='home'),
    path('landing/', views.landing, name='landing'),
    path('boucket/', views.boucket, name='boucket'),
    path('flower_basket/', views.flower_basket, name='flower_basket'),
    path('flower_box/', views.flower_box, name='flower_box'),
    path('delivery/', views.delivery, name='delivery'),
]