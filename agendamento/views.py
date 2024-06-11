from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from .models import Agendamento, Servico
from cliente.models import Animal, Client

@login_required
def agendar_servico(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        horario = request.POST.get('horario')
        observacao = request.POST.get('observacao')
        id_animal = request.POST.get('id_animal')
        id_servico = request.POST.get('id_servico')
        
        try:
            client = Client.objects.get(user=request.user)
            animal = Animal.objects.get(id=id_animal, client=client)
            servico = Servico.objects.get(id=id_servico)
            
            agendamento = Agendamento(
                data=data,
                horario=horario,
                observacao=observacao,
                id_animal=animal,
                id_cliente=request.user,
                id_servico=servico,
                finalizado=False
            )
            agendamento.save()
            messages.success(request, 'Serviço agendado com sucesso!')
            return redirect(reverse('criar_agenda'))

        except Client.DoesNotExist:
            messages.error(request, 'Cliente não encontrado.')
        except Animal.DoesNotExist:
            messages.error(request, 'Animal não encontrado ou você não tem permissão para agendar este animal.')
        except Servico.DoesNotExist:
            messages.error(request, 'Serviço não encontrado.')
        except Exception as e:
            messages.error(request, f'Erro ao agendar serviço: {e}')
    else:
        try:
            client = Client.objects.get(user=request.user)
            animais = Animal.objects.filter(client=client)
            servicos = Servico.objects.all()
        except Client.DoesNotExist:
            animais = []
            servicos = []
            messages.error(request, 'Cliente não encontrado.')

    return render(request, '../templates/agenda.html', {'animais': animais, 'servicos': servicos})


def criar_servico(request):
    if request.method == "GET":
        return render(request, 'servico.html')
    elif request.method == "POST":
        nome_servico = request.POST.get('nome_servico')
        descricao = request.POST.get('descricao')

        if not nome_servico or not descricao:
            messages.add_message(request, messages.ERROR, 'Os campos Nome do serviço e Descrição são obrigatórios.')
            return redirect(reverse('criar_servico'))

        servico = Servico(nome=nome_servico, descricao=descricao)
        servico.save()  # Salva o serviço no banco de dados

        messages.add_message(request, messages.SUCCESS, 'Serviço cadastrado com sucesso.')
        return redirect(reverse('criar_servico'))