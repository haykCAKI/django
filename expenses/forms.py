# expenses/forms.py
from django import forms
from .models import Expense
from datetime import datetime 
from decimal import Decimal, DecimalException

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['type_of_expense', 'spent_at', 'expense_value']
        widgets = {
            'spent_at': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_spent_at(self):
        spent_at = self.cleaned_data['spent_at']
        return spent_at.strftime('%Y-%m-%d')

    def clean_expense_value(self):
        expense_value = self.cleaned_data['expense_value']

        if expense_value is not None:
            try:
                expense_value = Decimal(str(expense_value).replace(',', '.'))
                if expense_value <= 0:
                    raise forms.ValidationError('O valor da despesa deve ser maior que zero.')
                return expense_value
            except (ValueError, DecimalException):
                raise forms.ValidationError('Insira um valor de despesa válido.')

    def clean(self):
        cleaned_data = super().clean()
        spent_at = cleaned_data.get('spent_at')
        expense_value = cleaned_data.get('expense_value')

        # Adicione lógica de validação personalizada aqui
        if spent_at is not None and expense_value is not None:
            # Garanta que spent_at seja um objeto date
            spent_at = datetime.strptime(spent_at, '%Y-%m-%d').date()

            today = datetime.now().date()
            if spent_at > today:
                self.add_error('spent_at', 'A data da despesa não pode estar no futuro.')