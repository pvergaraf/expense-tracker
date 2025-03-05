from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.conf import settings
from expenses.models import Expense
from todos.models import Todo
from datetime import datetime
import random
from .welcome_messages import WELCOME_MESSAGES

@login_required
def home(request):
    # Get current month's expenses
    current_month = datetime.now().replace(day=1)
    monthly_expenses = Expense.objects.filter(
        month_year__year=current_month.year,
        month_year__month=current_month.month
    )
    
    # Calculate expenses information
    total_expenses = monthly_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    budget = settings.MONTHLY_BUDGET
    remaining_budget = budget - total_expenses
    budget_percentage = (total_expenses / budget) * 100 if budget > 0 else 0
    
    # Get not completed todos
    pending_todos = Todo.objects.filter(completed=False).order_by('priority', '-created_at')[:5]
    
    # Get random welcome message
    welcome_message = random.choice(WELCOME_MESSAGES)
    
    context = {
        'expenses': monthly_expenses.order_by('-month_year'),
        'total_expenses': total_expenses,
        'budget': budget,
        'remaining_budget': remaining_budget,
        'budget_percentage': budget_percentage,
        'pending_todos': pending_todos,
        'welcome_message': welcome_message,
    }
    
    return render(request, 'chiwismo/home.html', context) 