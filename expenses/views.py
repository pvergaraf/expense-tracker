from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.conf import settings
from .forms import ExpenseForm
from .models import Expense
from datetime import datetime

# Create your views here.

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    
    return render(request, 'expenses/add_expense.html', {'form': form})

@login_required
def expense_list(request):
    current_month = datetime.now().replace(day=1)
    monthly_expenses = Expense.objects.filter(
        user=request.user,
        month_year__year=current_month.year,
        month_year__month=current_month.month
    )
    
    # Calculate total expenses for current month
    total_expenses = monthly_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Calculate budget information
    budget = settings.MONTHLY_BUDGET
    remaining_budget = budget - total_expenses
    budget_percentage = (total_expenses / budget) * 100 if budget > 0 else 0
    
    context = {
        'expenses': monthly_expenses.order_by('-month_year'),
        'total_expenses': total_expenses,
        'budget': budget,
        'remaining_budget': remaining_budget,
        'budget_percentage': budget_percentage,
    }
    
    return render(request, 'expenses/expense_list.html', context)

@login_required
def update_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully!')
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    
    return render(request, 'expenses/update_expense.html', {'form': form, 'expense': expense})

@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully!')
        return redirect('expense_list')
    
    return render(request, 'expenses/delete_expense.html', {'expense': expense})
