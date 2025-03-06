from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime, date
from calendar import monthrange
import json
from .models import Activity, ActivityCategory, ActivityLog

@login_required
def activity_list(request):
    """Admin view for managing activities"""
    activities = Activity.objects.filter(
        Q(created_by=request.user) | Q(shared=True)
    ).prefetch_related('categories')
    categories = ActivityCategory.objects.filter(created_by=request.user)
    
    return render(request, 'activities/admin/list.html', {
        'activities': activities,
        'categories': categories
    })

@login_required
def activity_detail(request, activity_id):
    """View activity details and all its logs"""
    activity = get_object_or_404(Activity, id=activity_id)
    if not activity.shared and activity.created_by != request.user:
        messages.error(request, "You don't have permission to view this activity.")
        return redirect('activities:list')
    
    logs = ActivityLog.objects.filter(activity=activity).select_related('user', 'category')
    return render(request, 'activities/detail.html', {
        'activity': activity,
        'logs': logs
    })

@login_required
def add_activity(request):
    """Add a new activity"""
    if request.method == 'POST':
        name = request.POST.get('name')
        shared = request.POST.get('shared') == 'on'
        
        if name:
            activity = Activity.objects.create(
                name=name,
                shared=shared,
                created_by=request.user
            )
            messages.success(request, 'Activity added successfully!')
        return redirect('activities:list')

@login_required
def edit_activity(request, activity_id):
    """Edit an existing activity"""
    activity = get_object_or_404(Activity, id=activity_id, created_by=request.user)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        shared = request.POST.get('shared') == 'on'
        
        if name:
            activity.name = name
            activity.shared = shared
            activity.save()
            messages.success(request, 'Activity updated successfully!')
        return redirect('activities:list')

@login_required
def delete_activity(request, activity_id):
    """Delete an activity"""
    activity = get_object_or_404(Activity, id=activity_id, created_by=request.user)
    activity.delete()
    messages.success(request, 'Activity deleted successfully!')
    return redirect('activities:list')

@login_required
def add_category(request):
    """Add a new activity category"""
    if request.method == 'POST':
        name = request.POST.get('name')
        activity_id = request.POST.get('activity')
        
        if name and activity_id:
            activity = get_object_or_404(Activity, id=activity_id)
            if activity.created_by == request.user:
                ActivityCategory.objects.create(
                    name=name,
                    activity=activity,
                    created_by=request.user
                )
                messages.success(request, 'Category added successfully!')
        return redirect('activities:list')

@login_required
def dashboard(request):
    """View activities dashboard with charts"""
    activities = Activity.objects.filter(
        Q(created_by=request.user) | Q(shared=True)
    ).prefetch_related('categories')
    
    year = datetime.now().year
    activity_data = {}
    
    for activity in activities:
        logs = activity.get_year_logs(year)
        log_dates = [log.logged_at for log in logs]
        categories = [category.name for category in activity.categories.all()]
        activity_data[activity.id] = {
            'name': activity.name,
            'categories': categories,
            'logs': [date.strftime('%Y-%m-%d') for date in log_dates]
        }
    
    return render(request, 'activities/dashboard.html', {
        'activities': activities,
        'activity_data': json.dumps(activity_data),
        'year': year
    })

@login_required
def toggle_log(request):
    """Add a new activity log"""
    if request.method == 'POST':
        try:
            # Try to parse JSON data first
            data = json.loads(request.body)
            activity_id = data.get('activity_id')
            log_date = data.get('log_date', date.today().isoformat())
            category_id = data.get('category_id')
        except json.JSONDecodeError:
            # Fall back to form data if not JSON
            activity_id = request.POST.get('activity_id')
            log_date = request.POST.get('log_date', date.today().isoformat())
            category_id = request.POST.get('category_id')

        if not activity_id:
            return JsonResponse({'error': 'Activity ID is required'}, status=400)

        activity = get_object_or_404(Activity, id=activity_id)
        
        if not activity.shared and activity.created_by != request.user:
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        # Convert log_date string to date object
        try:
            logged_at = datetime.strptime(log_date, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'error': 'Invalid date format'}, status=400)
        
        # If a category is specified, verify it belongs to this activity
        category = None
        if category_id:
            category = get_object_or_404(ActivityCategory, id=category_id, activity=activity)
        
        # Create new log
        ActivityLog.objects.create(
            activity=activity,
            user=request.user,
            logged_at=logged_at,
            category=category
        )
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
def get_activity_categories(request, activity_id):
    """API endpoint to get categories for an activity"""
    activity = get_object_or_404(Activity, id=activity_id)
    if not activity.shared and activity.created_by != request.user:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    categories = activity.categories.all()
    return JsonResponse([{
        'id': category.id,
        'name': category.name
    } for category in categories], safe=False)

@login_required
def edit_log(request, log_id):
    """Edit an existing activity log."""
    log = get_object_or_404(ActivityLog, id=log_id)
    
    # Check if user has permission to edit this log
    if log.user != request.user:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            log_date = data.get('log_date')
            category_id = data.get('category_id')
            
            # Validate date format
            try:
                log_date = datetime.strptime(log_date, '%Y-%m-%d').date()
            except (ValueError, TypeError):
                return JsonResponse({'error': 'Invalid date format'}, status=400)
            
            # Update log
            log.logged_at = log_date
            if category_id:
                category = get_object_or_404(ActivityCategory, id=category_id)
                if category.activity_id != log.activity_id:
                    return JsonResponse({'error': 'Invalid category'}, status=400)
                log.category = category
            log.save()
            
            return JsonResponse({'success': True})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
def delete_log(request, log_id):
    """Delete an activity log."""
    log = get_object_or_404(ActivityLog, id=log_id)
    
    # Check if user has permission to delete this log
    if log.user != request.user:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    if request.method == 'POST':
        log.delete()
        return JsonResponse({'success': True})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
