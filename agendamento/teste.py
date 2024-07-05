@login_required
def listar_agendamentos(request):
    agendamentos = Agendamento.objects.all()

    if request.user.cargo == 'W':
        agendamentos = agendamentos
    else:
        agendamentos = agendamentos.filter(id_cliente=request.user)

    if request.method == 'GET':
        form = AgendamentoFilterForm(request.GET)
        if form.is_valid():
            data_inicio = form.cleaned_data.get('data_inicio')
            data_fim = form.cleaned_data.get('data_fim')
            status = form.cleaned_data.get('status')

            if data_inicio:
                agendamentos = agendamentos.filter(data__gte=data_inicio)
            if data_fim:
                agendamentos = agendamentos.filter(data__lte=data_fim)
            if status:
                if status == 'Pendente':
                    agendamentos = agendamentos.filter(finalizado=False)
                elif status == 'Finalizado':
                    agendamentos = agendamentos.filter(finalizado=True)
    else:
        form = AgendamentoFilterForm()

    agendamentos = agendamentos.order_by('-data', '-horario_inicio')

    context = {
        'agendamentos': agendamentos,
        'form': form,
    }
    return render(request, 'listar_agendamentos.html', context)
