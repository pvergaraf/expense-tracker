from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('', views.expense_list, name='list'),
    path('add/', views.add_expense, name='add'),
    path('<int:pk>/update/', views.update_expense, name='update'),
    path('<int:pk>/delete/', views.delete_expense, name='delete'),
] 