from django.urls import path
from . import views

app_name = 'shopping'

urlpatterns = [
    path('', views.shopping_list, name='list'),
    path('add/', views.add_item, name='add'),
    path('toggle/<int:item_id>/', views.toggle_purchased, name='toggle'),
] 