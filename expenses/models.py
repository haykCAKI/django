from django.db import models

# Create your models here.
class Expense(models.Model):
    type_of_expense = models.CharField(max_length = 255)
    spent_at = models.DateField()
    expense_value = models.DecimalField(max_digits = 10, decimal_places = 2)