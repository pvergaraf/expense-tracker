from django import forms
from .models import Expense
from django.utils import timezone

class ExpenseForm(forms.ModelForm):
    month_year = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'month',
                'value': timezone.now().strftime('%Y-%m'),
            }
        ),
        input_formats=['%Y-%m']
    )
    
    description = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Expense
        fields = ['amount', 'month_year', 'description']

    def clean_month_year(self):
        # Convert the month-year to the first day of the month
        month_year = self.cleaned_data['month_year']
        if isinstance(month_year, str):
            # If it's a string (YYYY-MM format), convert it to date
            try:
                year, month = map(int, month_year.split('-'))
                from datetime import date
                month_year = date(year, month, 1)
            except (ValueError, TypeError):
                raise forms.ValidationError('Please enter a valid month and year')
        return month_year.replace(day=1) 