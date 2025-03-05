from django.urls import path
from . import views

app_name = 'todos'

urlpatterns = [
    path('', views.todo_list, name='list'),
    path('add/', views.add_todo, name='add'),
    path('<int:pk>/update/', views.update_todo, name='update'),
    path('<int:pk>/delete/', views.delete_todo, name='delete'),
    path('<int:pk>/toggle/', views.toggle_todo, name='toggle'),
] 