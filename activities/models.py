from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Activity(models.Model):
    """Activity model for tracking recurring activities"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Emoji or icon name")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    shared = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Activities"
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def get_logs_for_year(self, year=None):
        """Get all logs for a specific year"""
        if year is None:
            year = timezone.now().year
        return self.activitylog_set.filter(date__year=year)
    
    def get_last_log(self):
        """Get the most recent log"""
        return self.activitylog_set.order_by('-date').first()


class ActivityLog(models.Model):
    """Log of when an activity was performed"""
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        # Ensure a user can only log an activity once per day
        unique_together = ['activity', 'user', 'date']

    def __str__(self):
        return f"{self.activity.name} - {self.date}"
