from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Todo
from .forms import TodoForm
from django.db import models

# Create your views here.

@login_required
def todo_list(request):
    # Get todos where user is either creator or assignee
    todos = Todo.objects.filter(
        models.Q(created_by=request.user) |
        models.Q(assigned_to=request.user)
    ).distinct()
    
    context = {
        'todos': todos,
        'pending_todos': todos.filter(completed=False),
        'completed_todos': todos.filter(completed=True)
    }
    return render(request, 'todos/todo_list.html', context)

@login_required
def add_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.created_by = request.user
            todo.save()
            # Save many-to-many relationships
            form.save_m2m()
            messages.success(request, 'Todo created successfully!')
            # Check if we should redirect to home
            next_page = request.GET.get('next')
            if next_page == 'home':
                return redirect('home')
            return redirect('todos:list')
    else:
        form = TodoForm()
    
    return render(request, 'todos/todo_form.html', {'form': form, 'title': 'Add Todo'})

@login_required
def update_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Todo updated successfully!')
            return redirect('todos:list')
    else:
        form = TodoForm(instance=todo)
    
    return render(request, 'todos/todo_form.html', {
        'form': form,
        'todo': todo,
        'title': 'Update Todo'
    })

@login_required
def delete_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    
    if request.method == 'POST':
        todo.delete()
        messages.success(request, 'Todo deleted successfully!')
        return redirect('todos:list')
    
    return render(request, 'todos/todo_confirm_delete.html', {'todo': todo})

@login_required
def toggle_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.completed = not todo.completed
    todo.completed_at = timezone.now() if todo.completed else None
    todo.save()
    
    if todo.completed:
        messages.success(request, f'Task "{todo.title}" marked as completed! 🎉')
    else:
        messages.info(request, f'Task "{todo.title}" marked as pending')
    
    return redirect('todos:list')
