from django.db import models
from django.contrib.auth.models import User

class Activity(models.Model):
    name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    shared = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Activities"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_year_logs(self, year):
        """Get all logs for this activity in a specific year"""
        return self.activitylog_set.filter(logged_at__year=year)

    def get_last_log(self):
        """Get the most recent log for this activity"""
        return self.activitylog_set.first()

class ActivityCategory(models.Model):
    name = models.CharField(max_length=100)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='categories')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Activity Categories"
        ordering = ['name']
        unique_together = ['name', 'activity']  # Categories must be unique per activity

    def __str__(self):
        return f"{self.activity.name} - {self.name}"

class ActivityLog(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(ActivityCategory, on_delete=models.SET_NULL, null=True, blank=True)
    logged_at = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-logged_at', '-created_at']

    def __str__(self):
        return f"{self.activity.name} - {self.logged_at}"
