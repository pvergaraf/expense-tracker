from django.urls import path
from . import views

app_name = 'activities'

urlpatterns = [
    # Admin views
    path('admin/', views.activity_list, name='list'),
    path('admin/<int:activity_id>/', views.activity_detail, name='detail'),
    path('admin/add/', views.add_activity, name='add'),
    path('admin/<int:activity_id>/edit/', views.edit_activity, name='edit'),
    path('admin/<int:activity_id>/delete/', views.delete_activity, name='delete'),
    path('admin/category/add/', views.add_category, name='add_category'),
    
    # Dashboard view
    path('', views.dashboard, name='dashboard'),
    
    # API endpoints
    path('toggle-log/', views.toggle_log, name='toggle_log'),
    path('api/categories/<int:activity_id>/', views.get_activity_categories, name='get_categories'),
    path('logs/<int:log_id>/edit/', views.edit_log, name='edit_log'),
    path('logs/<int:log_id>/delete/', views.delete_log, name='delete_log'),
] 