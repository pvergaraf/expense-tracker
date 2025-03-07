from django import forms
from .models import Activity, ActivityLog

class ActivityForm(forms.ModelForm):
    """Form for creating and editing activities"""
    class Meta:
        model = Activity
        fields = ['name', 'description', 'icon', 'shared']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter activity name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter activity description'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter an emoji (e.g. 🏃‍♂️, 📚)'}),
            'shared': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        help_texts = {
            'icon': 'Add an emoji to represent this activity (e.g. 🏃‍♂️, 🏊‍♀️, 📚)',
            'shared': 'If checked, this activity will be visible to all users.',
        }

class ActivityLogForm(forms.ModelForm):
    """Form for logging an activity"""
    class Meta:
        model = ActivityLog
        fields = ['date', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add any notes about this activity (optional)'
            }),
        } 