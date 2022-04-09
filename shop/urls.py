from django.urls import path
from . import views

urlpatterns = [

    path('', views.product_list, name='product_list'),
    path('register/', views.register, name='register'),
    path('<category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug>/', views.product_detail, name='product_detail'),



]
