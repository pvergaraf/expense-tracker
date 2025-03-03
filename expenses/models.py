from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    month_year = models.DateField()  # We'll use the first day of month
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.month_year.strftime('%B %Y')} - ${self.amount} - {self.description[:30]}"
