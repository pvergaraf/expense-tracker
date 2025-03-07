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
    shared = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Todo
        fields = ['title', 'description', 'due_date', 'shared', 'assigned_to']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }