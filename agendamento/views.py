from datetime import timedelta, datetime, time
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from .models import Agendamento, Servico
from cliente.models import Animal, Client
from django.db.models import Q

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
    """
    View para agendar um serviço para um animal de estimação.
    """
    try:
        client = get_object_or_404(Client, user=request.user)
        animais = Animal.objects.filter(client=client, ativo=True)
        if not animais.exists():
            messages.error(request, 'Você não tem nenhum animal ativo cadastrado. Por favor, cadastre um pet.')
            return redirect('register_pet')
    except Exception as e:
        messages.error(request, 'Cliente não encontrado. Por favor, registre suas informações de cliente primeiro.')
        return redirect('register_client_info')

    try:
        servicos = Servico.objects.all()
    except Exception as e:
        messages.error(request, f'Erro ao obter lista de serviços: {e}')
        servicos = []

    horarios_disponiveis = []
    data = request.POST.get('data', '')
    id_servico = request.POST.get('id_servico', '')

    if request.method == 'POST':
        if 'submit_horarios' in request.POST:
            try:
                data = request.POST.get('data')
                servico = Servico.objects.get(id=id_servico)
                duracao = servico.duracao

                # Calcular horários disponíveis com base na duração do serviço
                data_obj = datetime.strptime(data, '%Y-%m-%d').date()
                horarios_disponiveis = calcular_horarios_disponiveis(data_obj, duracao)

            except Servico.DoesNotExist:
                messages.error(request, 'Serviço não encontrado.')
            except Exception as e:
                messages.error(request, f'Erro ao calcular horários disponíveis: {e}')
        elif 'submit_agendamento' in request.POST:
            horario_str = request.POST.get('horario')
            observacao = request.POST.get('observacao')
            id_animal = request.POST.get('id_animal')

            try:
                data = request.POST.get('data')
                horario_inicio = datetime.strptime(horario_str, '%H:%M').time()

                animal = Animal.objects.get(id=id_animal, client=client)
                servico = Servico.objects.get(id=id_servico)
                duracao = servico.duracao

                # Calcular o horário de término
                data_obj = datetime.strptime(data, '%Y-%m-%d').date()
                horario_fim = (datetime.combine(data_obj, horario_inicio) + duracao).time()

                # Verificar se o horário está disponível para qualquer animal
                if not is_horario_disponivel(data_obj, horario_inicio, horario_fim):
                    messages.error(request, 'Já existe um agendamento para este horário.')
                    return redirect(reverse('criar_agenda'))

                agendamento = Agendamento(
                    data=data_obj,
                    horario_inicio=horario_inicio,
                    horario_fim=horario_fim,
                    observacao=observacao,
                    animal=animal,
                    cliente=request.user,
                    servico=servico,
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

    return render(request, 'agenda.html', {
        'animais': animais,
        'servicos': servicos,
        'horarios_disponiveis': horarios_disponiveis,
        'data': data,
        'id_servico': id_servico
    })




def calcular_horarios_disponiveis(data, duracao):
    """
    Calcula os horários disponíveis para agendamento com base na duração do serviço.
    
    :param data: Data para a qual os horários são calculados.
    :param duracao: Duração do serviço como um objeto timedelta.
    :return: Lista de horários disponíveis.
    """
    horarios_disponiveis = []
    horario_atual = datetime.combine(data, time(8, 0))  # Começa às 08:00

    while horario_atual.time() < time(18, 0):  # Termina às 18:00
        horarios_disponiveis.append(horario_atual.time())
        horario_atual += duracao

    return horarios_disponiveis



def is_horario_disponivel(data, horario_inicio, horario_fim):
    """
    Verifica se o intervalo de tempo está disponível para agendamento.
    
    :param data: Data do agendamento.
    :param horario_inicio: Horário de início do agendamento.
    :param horario_fim: Horário de término do agendamento.
    :return: True se o intervalo está disponível, False caso contrário.
    """
    agendamentos_existentes = Agendamento.objects.filter(
        data=data
    ).filter(
        Q(horario_inicio__lt=horario_fim, horario_fim__gt=horario_inicio)
    )

    return not agendamentos_existentes.exists()






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
            agendamentos = Agendamento.objects.all().order_by('-data', '-horario_inicio')
        else:  # Assumimos que qualquer outro cargo, especialmente 'C', deve visualizar apenas seus agendamentos
            agendamentos = Agendamento.objects.filter(id_cliente=request.user).order_by('-data', '-horario_inicio')
    except Exception as e:
        messages.error(request, f'Erro ao obter agendamentos: {e}')
        agendamentos = []

    return render(request, 'listar_agendamentos.html', {'agendamentos': agendamentos})
