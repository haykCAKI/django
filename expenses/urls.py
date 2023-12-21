# expenses/urls.py
from django.urls import path
from .views import expense_list, add_expense, delete_expense, expense_chart_pie, edit_expense, expense_chart_bar


urlpatterns = [
    path('list/', expense_list, name='expense_list'),
    path('add/', add_expense, name='add_expense'),
    path('expense_chart_pie/', expense_chart_pie, name='expense_chart_pie'),
    path('expense_chart_bar/', expense_chart_bar, name='expense_chart_bar'),
    path('delete/<int:expense_id>/', delete_expense, name='delete_expense'),
    path('edit<int:expense_id>/', edit_expense, name='edit_expense'),
]
