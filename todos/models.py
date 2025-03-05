from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_todos')
    assigned_to = models.ManyToManyField(User, related_name='assigned_todos', blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    priority = models.IntegerField(default=0)  # Higher number = higher priority

    class Meta:
        ordering = ['-priority', 'due_date', '-created_at']

    def __str__(self):
        return self.title
