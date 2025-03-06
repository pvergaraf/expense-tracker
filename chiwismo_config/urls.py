"""
URL configuration for chiwismo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from chiwismo import views as chiwismo_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', chiwismo_views.home, name='home'),
    path('expenses/', include('expenses.urls', namespace='expenses')),
    path('todos/', include('todos.urls', namespace='todos')),
    path('shopping/', include('shopping.urls')),
    path('activities/', include('activities.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
