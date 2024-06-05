# views.py
from django.shortcuts import render, redirect
from .forms import AgendamentoForm
from django.contrib import messages

def agenda_view(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Agendamento realizado com sucesso!")
            return redirect('agenda')
        else:
            messages.error(request, "Erro ao realizar o agendamento.")
    else:
        form = AgendamentoForm()

    return render(request, '../templates/agenda.html', {'form': form})


# Create your views here.
# def agenda(request):
#     return render(request, '../templates/agenda.html')

