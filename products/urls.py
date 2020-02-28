from django.urls import path, include
from products import views

urlpatterns = [
    path('<int:product_id>/', views.product, name='product')
]