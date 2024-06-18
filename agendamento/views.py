from datetime import timedelta, datetime, time
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from .models import Agendamento, Servico
from cliente.models import Animal, Client

@login_required
def criar_servico(request):
    if request.user.cargo != 'W':
        messages.add_message(request, messages.ERROR, 'Você não tem permissão para acessar esta página.')
        return redirect('inicio')  # Redireciona para a página inicial ou outra página apropriada
    
    if request.method == "GET":
        return render(request, 'servico.html')
    elif request.method == "POST":
        nome_servico = request.POST.get('nome_servico')
        descricao = request.POST.get('descricao')
        duracao = request.POST.get('duracao')

        if not nome_servico or not descricao or not duracao:
            messages.add_message(request, messages.ERROR, 'Todos os campos são obrigatórios.')
            return redirect(reverse('criar_servico'))

        try:
            # Converte a duração para um objeto timedelta
            hours, minutes = map(int, duracao.split(':'))
            duracao_timedelta = timedelta(hours=hours, minutes=minutes)

            servico = Servico(nome=nome_servico, descricao=descricao, duracao=duracao_timedelta)
            servico.save()  # Salva o serviço no banco de dados

            messages.add_message(request, messages.SUCCESS, 'Serviço cadastrado com sucesso.')
            return redirect(reverse('criar_servico'))
        except ValueError:
            messages.add_message(request, messages.ERROR, 'Formato de duração inválido.')
            return redirect(reverse('criar_servico'))

@login_required
def agendar_servico(request):
    try:
        client = get_object_or_404(Client, user=request.user)
        animais = Animal.objects.filter(client=client)
    except Client.DoesNotExist:
        messages.error(request, 'Cliente não encontrado. Por favor, registre suas informações de cliente primeiro.')
        return redirect('register_client_info')
    except Exception as e:
        messages.error(request, f'Erro ao obter informações do cliente: {e}')
        animais = []

    try:
        servicos = Servico.objects.all()
    except Exception as e:
        messages.error(request, f'Erro ao obter lista de serviços: {e}')
        servicos = []

    horarios_disponiveis = []
    if request.method == 'POST':
        if 'submit_horarios' in request.POST:
            data_str = request.POST.get('data')
            id_servico = request.POST.get('id_servico')

            try:
                data = datetime.strptime(data_str, '%Y-%m-%d').date()
                servico = Servico.objects.get(id=id_servico)
                duracao = servico.duracao

                # Calcular horários disponíveis com base na duração do serviço
                horarios_disponiveis = calcular_horarios_disponiveis(data, duracao)

            except Servico.DoesNotExist:
                messages.error(request, 'Serviço não encontrado.')
            except Exception as e:
                messages.error(request, f'Erro ao calcular horários disponíveis: {e}')
        elif 'submit_agendamento' in request.POST:
            data_str = request.POST.get('data')
            horario_str = request.POST.get('horario')
            observacao = request.POST.get('observacao')
            id_animal = request.POST.get('id_animal')
            id_servico = request.POST.get('id_servico')

            try:
                data = datetime.strptime(data_str, '%Y-%m-%d').date()
                horario = datetime.strptime(horario_str, '%H:%M').time()

                animal = Animal.objects.get(id=id_animal, client=client)
                servico = Servico.objects.get(id=id_servico)
                duracao = servico.duracao

                # Calcular o horário de término
                horario_inicio = datetime.combine(data, horario)
                horario_fim = horario_inicio + duracao

                # Verificar se o horário está disponível
                agendamentos_existentes = Agendamento.objects.filter(
                    id_animal=animal,
                    data=data
                ).exclude(
                    horario__gte=horario_fim.time(),
                    horario__lt=(horario_inicio - duracao).time()
                )

                if agendamentos_existentes.exists():
                    messages.error(request, 'Já existe um agendamento para este horário.')
                    return redirect(reverse('criar_agenda'))

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
                return redirect('inicio')
            except Animal.DoesNotExist:
                messages.error(request, 'Animal não encontrado ou você não tem permissão para agendar este animal.')
            except Servico.DoesNotExist:
                messages.error(request, 'Serviço não encontrado.')
            except Exception as e:
                messages.error(request, f'Erro ao agendar serviço: {e}')

    return render(request, '../templates/agenda.html', {
        'animais': animais,
        'servicos': servicos,
        'horarios_disponiveis': horarios_disponiveis,
        'data': request.POST.get('data') if request.method == 'POST' else '',
        'id_servico': request.POST.get('id_servico') if request.method == 'POST' else ''
    })

def calcular_horarios_disponiveis(data, duracao):
    horarios_disponiveis = []
    horario_atual = datetime.combine(data, time(8, 0))  # Começa às 08:00

    while horario_atual.time() < time(18, 0):  # Termina às 18:00
        horarios_disponiveis.append(horario_atual.time())
        horario_atual += duracao

    return horarios_disponiveis

@login_required
def listar_agendamentos(request):
    if request.method == "POST":
        agendamento_id = request.POST.get('agendamento_id')
        action = request.POST.get('action')

        try:
            agendamento = get_object_or_404(Agendamento, id=agendamento_id)

            if action == 'finalizar':
                agendamento.finalizado = True
                agendamento.save()
                messages.success(request, 'Agendamento finalizado com sucesso.')

            elif action == 'cancelar':
                agendamento.delete()
                messages.error(request, 'Agendamento cancelado com sucesso.')

            elif action == 'reabrir':
                agendamento.finalizado = False
                agendamento.save()
                messages.success(request, 'Agendamento aberto com sucesso.')

        except Exception as e:
            messages.error(request, f'Erro ao processar agendamento: {e}')

    try:
        if request.user.cargo == 'W':  # Verifica se o usuário tem o cargo 'W'
            agendamentos = Agendamento.objects.all().order_by('-data', '-horario')
        else:  # Assumimos que qualquer outro cargo, especialmente 'C', deve visualizar apenas seus agendamentos
            agendamentos = Agendamento.objects.filter(id_cliente=request.user).order_by('-data', '-horario')
    except Exception as e:
        messages.error(request, f'Erro ao obter agendamentos: {e}')
        agendamentos = []

    return render(request, 'listar_agendamentos.html', {'agendamentos': agendamentos})
