from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
import json
from datetime import datetime

from .models import Activity, ActivityLog
from .forms import ActivityForm, ActivityLogForm

@login_required
def activity_list(request):
    """View to list all activities"""
    # Get activities created by the user or shared with everyone
    activities = Activity.objects.filter(
        Q(created_by=request.user) | Q(shared=True)
    ).order_by('name')
    
    return render(request, 'activities/activity_list.html', {
        'activities': activities
    })

@login_required
def activity_detail(request, activity_id):
    """View to show activity details and logs"""
    activity = get_object_or_404(Activity, id=activity_id)
    
    # Check if user has access to this activity
    if not (activity.created_by == request.user or activity.shared):
        messages.error(request, "You don't have permission to view this activity.")
        return redirect('activities:list')
    
    # Get logs for the current year
    current_year = timezone.now().year
    logs = activity.get_logs_for_year(current_year)
    
    return render(request, 'activities/activity_detail.html', {
        'activity': activity,
        'logs': logs,
        'year': current_year
    })

@login_required
def activity_create(request):
    """View to create a new activity"""
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.created_by = request.user
            activity.save()
            messages.success(request, f'Activity "{activity.name}" created successfully!')
            return redirect('activities:detail', activity_id=activity.id)
    else:
        form = ActivityForm()
    
    return render(request, 'activities/activity_form.html', {
        'form': form,
        'title': 'Create Activity'
    })

@login_required
def activity_edit(request, activity_id):
    """View to edit an activity"""
    activity = get_object_or_404(Activity, id=activity_id)
    
    # Check if user has permission to edit
    if activity.created_by != request.user:
        messages.error(request, "You don't have permission to edit this activity.")
        return redirect('activities:list')
    
    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            messages.success(request, f'Activity "{activity.name}" updated successfully!')
            return redirect('activities:detail', activity_id=activity.id)
    else:
        form = ActivityForm(instance=activity)
    
    return render(request, 'activities/activity_form.html', {
        'form': form,
        'activity': activity,
        'title': 'Edit Activity'
    })

@login_required
def activity_delete(request, activity_id):
    """View to delete an activity"""
    activity = get_object_or_404(Activity, id=activity_id)
    
    # Check if user has permission to delete
    if activity.created_by != request.user:
        messages.error(request, "You don't have permission to delete this activity.")
        return redirect('activities:list')
    
    if request.method == 'POST':
        activity_name = activity.name
        activity.delete()
        messages.success(request, f'Activity "{activity_name}" deleted successfully!')
        return redirect('activities:list')
    
    return render(request, 'activities/activity_confirm_delete.html', {
        'activity': activity
    })

@login_required
def log_activity(request, activity_id):
    """View to log an activity"""
    activity = get_object_or_404(Activity, id=activity_id)
    
    # Check if user has access to this activity
    if not (activity.created_by == request.user or activity.shared):
        messages.error(request, "You don't have permission to log this activity.")
        return redirect('activities:list')
    
    if request.method == 'POST':
        form = ActivityLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.activity = activity
            log.user = request.user
            log.save()
            messages.success(request, f'Activity "{activity.name}" logged successfully!')
            return redirect('activities:detail', activity_id=activity.id)
    else:
        form = ActivityLogForm(initial={'date': timezone.now().date()})
    
    return render(request, 'activities/log_form.html', {
        'form': form,
        'activity': activity
    })

@login_required
def delete_log(request, log_id):
    """View to delete an activity log"""
    log = get_object_or_404(ActivityLog, id=log_id)
    activity = log.activity
    
    # Check if user has permission to delete this log
    if log.user != request.user:
        messages.error(request, "You don't have permission to delete this log.")
        return redirect('activities:detail', activity_id=activity.id)
    
    if request.method == 'POST':
        log.delete()
        messages.success(request, f'Log for {activity.name} on {log.date} deleted successfully!')
        return redirect('activities:detail', activity_id=activity.id)
    
    return render(request, 'activities/log_confirm_delete.html', {
        'log': log,
        'activity': activity
    })

@login_required
def dashboard(request):
    """View for the activity dashboard with charts"""
    # Get activities created by the user or shared with everyone
    activities = Activity.objects.filter(
        Q(created_by=request.user) | Q(shared=True)
    ).order_by('name')
    
    # Prepare data for charts
    activity_data = {}
    current_year = timezone.now().year
    
    for activity in activities:
        logs = activity.get_logs_for_year(current_year)
        last_log = activity.get_last_log()
        
        # Convert logs to weekly data
        weekly_data = {}
        for log in logs:
            # Get ISO week number (1-53)
            year, week, _ = log.date.isocalendar()
            # Only count if it's in the current year
            if year == current_year:
                weekly_data[week] = weekly_data.get(week, 0) + 1
                print(f"Log date: {log.date}, ISO Week: {week}")
        
        # Convert to list format for Chart.js
        weeks_data = []
        max_week = max(weekly_data.keys()) if weekly_data else 53
        for week in range(1, max_week + 1):  # Weeks 1-53 (ISO weeks can go up to 53)
            weeks_data.append(weekly_data.get(week, 0))
        
        # Use string ID as key
        str_id = str(activity.id)
        activity_data[str_id] = {
            'name': activity.name,
            'icon': activity.icon or '',
            'last_log': last_log.date.strftime('%Y-%m-%d') if last_log else None,
            'weekly_logs': weeks_data
        }
        print(f"Activity {activity.name} data:")
        print(f"- Weekly data: {weekly_data}")
        print(f"- Weeks data array: {weeks_data}")
    
    # Convert to JSON for JavaScript
    activity_data_json = json.dumps(activity_data)
    
    return render(request, 'activities/dashboard.html', {
        'activities': activities,
        'activity_data': activity_data,
        'activity_data_json': activity_data_json,
        'year': current_year
    })
