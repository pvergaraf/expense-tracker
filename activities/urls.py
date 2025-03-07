from django.urls import path
from . import views

app_name = 'activities'

urlpatterns = [
    # Activity views
    path('', views.dashboard, name='dashboard'),
    path('list/', views.activity_list, name='list'),
    path('<int:activity_id>/', views.activity_detail, name='detail'),
    path('create/', views.activity_create, name='create'),
    path('<int:activity_id>/edit/', views.activity_edit, name='edit'),
    path('<int:activity_id>/delete/', views.activity_delete, name='delete'),
    
    # Log views
    path('<int:activity_id>/log/', views.log_activity, name='log'),
    path('log/<int:log_id>/delete/', views.delete_log, name='delete_log'),
] 