from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Q
from .models import Expense
from .forms import ExpenseForm
from django.contrib import messages
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import matplotlib 
matplotlib.use('Agg')
# Create your views here.

def expense_list(request):
    order_by_param = request.GET.get('order_by', 'spent_at')

    if order_by_param not in ['spent_at', 'type_of_expense', 'expense_value']:
        order_by_param = 'spent_at'

    search_query = request.GET.get('search', '')
    
    if search_query:
        expenses = Expense.objects.filter(
            Q(type_of_expense__icontains=search_query) |
            Q(spent_at__icontains=search_query)
        ).order_by(order_by_param)
    else:
        expenses = Expense.objects.all().order_by(order_by_param)

    context = {
        'expenses': expenses,
        'total_expense': expenses.aggregate(Sum('expense_value'))['expense_value__sum'],
        'order_by': order_by_param,
        'search_query': search_query,
    }

    # the program will return a render in the expense_list.html the values expenses and total_expense
    return render(request, 'expense_list.html', context)

def add_expense(request):
    # if the method Post its safe to access, the program will aplicating the value form
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        messages.success(request, 'Despesa adicionada com sucesso.')
        # id de form is validated, the program will saving the data and return to list
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        # this else maybe i should to programming a value error if the form going to a error 404 or 303.
        form = ExpenseForm()
    return render(request, 'add_expense.html', {'form':form})

def expense_chart_pie(request):
    expenses = Expense.objects.values('type_of_expense').annotate(total=Sum('expense_value'))

    # Criação do gráfico de pizza
    labels = [expense['type_of_expense'] for expense in expenses]
    values = [expense['total'] for expense in expenses]

    plt.figure(figsize=(8, 8))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

    # Salva a imagem em um buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convertendo a imagem em base64 para exibir no template
    chart_data = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()

    context = {'chart_data': chart_data}
    
    # Renderize o template
    return render(request, 'expense_chart_pie.html', context)

def expense_chart_bar(request):
    # Crie uma figura do Matplotlib
    plt.figure(figsize=(10, 6))

    # Consulte o banco de dados para obter dados
    expenses = Expense.objects.values('type_of_expense').annotate(total=Sum('expense_value'))

    # Extraia rótulos e valores para o gráfico
    labels = [expense['type_of_expense'] for expense in expenses]
    values = [expense['total'] for expense in expenses]

    # Crie um gráfico de barras
    plt.bar(labels, values, color='blue')

    # Adicione rótulos e título
    plt.xlabel('Tipo de Despesa')
    plt.ylabel('Total Gasto')
    plt.title('Despesas por Tipo')

    # Salve a figura em um buffer de BytesIO
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Codifique a imagem em base64 para incorporá-la em uma tag HTML
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    # Passe a imagem codificada para o template
    context = {'image_base64': image_base64}

    return render(request, 'expense_chart_bar.html', context)


def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)
    expense.delete()
    messages.success(request, 'Despesa excluída com sucesso.')
    return redirect('expense_list')

def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    
    return render(request, 'edit_expense.html', {'form': form, 'expense': expense})