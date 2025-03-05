from django import forms
from .models import Todo
from django.contrib.auth.models import User

class TodoForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    assigned_to = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    priority = forms.IntegerField(
        min_value=0,
        max_value=5,
        initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Todo
        fields = ['title', 'description', 'due_date', 'priority', 'assigned_to']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        } 