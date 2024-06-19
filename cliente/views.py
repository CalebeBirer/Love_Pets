from django.shortcuts import render, redirect, get_object_or_404
from .models import Users, Animal, Client
from agendamento.models import Agendamento
from django.contrib import messages
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import UserForm, ClientForm, AnimalForm

def inicio(request):
    return render(request, '../templates/inicio.html')

def login(request):
    return render(request, '../templates/login.html')


def register_client(request):
    if request.method == "GET":        
        return render(request, 'register_client.html')
    if request.method == "POST":
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirma_senha = request.POST.get('confirma_senha')

        user = Users.objects.filter(email=email)

        if user.exists():            
            messages.add_message(request, messages.ERROR, 'E-mail ja cadastrado em outro momento')
            return redirect(reverse('register_client'))                
        elif (senha != confirma_senha):
            messages.add_message(request, messages.ERROR, 'As senhas digitas não conferem')
            return redirect(reverse('register_client'))
        elif (senha == ''):
            messages.add_message(request, messages.ERROR, 'O campo senha é obrigatorio')
            return redirect(reverse('register_client'))
        
        user = Users.objects.create_user(username=email, 
                                        email=email, 
                                        password=senha, 
                                        first_name=nome, 
                                        last_name=sobrenome,
                                        cargo="C")

        messages.add_message(request, messages.SUCCESS, 'Usuario cadastrado com sucesso')
        return redirect(reverse('login'))


def login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            # redirect redireciona para a pagina desejada e o reverse tranforma o nome em um URL
            messages.add_message(request, messages.ERROR, 'Usuario ja logado')
            return redirect(reverse('listar_editar_usuario')) 
        return render(request, 'login.html')
    elif request.method == "POST": 
        login = request.POST.get('email')
        senha = request.POST.get('senha')

        user = auth.authenticate(username=login, password=senha)

        if not user:
            messages.add_message(request, messages.ERROR, 'Usuario ou senha invalidos')
            return redirect(reverse('login'))
        
        auth.login(request,user)
        messages.add_message(request, messages.SUCCESS, 'Usuario logado com Sucesso')        
        return redirect(reverse('login'))
    
def logout(request):
    request.session.flush()
    messages.add_message(request, messages.WARNING, 'Logout efetuado com sucesso')
    return redirect(reverse('login'))


@login_required
def register_pet(request):
    try:
        client = get_object_or_404(Client, user=request.user)
    except:
        messages.error(request, 'Você precisa registrar suas informações de cliente antes de cadastrar um pet.')
        return redirect('register_client_info')  # Redireciona para a página de registro de informações do cliente

    if request.method == "POST":
        nome_pet = request.POST.get('nome_pet')
        raca = request.POST.get('raca')
        tipo_pelo = request.POST.get('tipo_pelo')
        porte = request.POST.get('porte')

        if not nome_pet or not raca or not tipo_pelo or not porte:
            messages.add_message(request, messages.ERROR, 'Todos os campos são obrigatórios.')
            return redirect(reverse('register_pet'))

        animal = Animal(
            nome=nome_pet,
            raca=raca,
            tipo_pelo=tipo_pelo,
            porte=porte,
            client=client
        )

        animal.save()

        messages.add_message(request, messages.SUCCESS, 'Pet cadastrado com sucesso')
        return redirect(reverse('inicio'))

    choices_pelo = Animal._meta.get_field('tipo_pelo').choices
    choices_porte = Animal._meta.get_field('porte').choices
    context = {
        'choices_pelo': choices_pelo,
        'choices_porte': choices_porte
    }
    return render(request, 'register_pet.html', context)        

@login_required
def register_client_info(request):
    if request.method == "POST":
        cpf = request.POST.get('cpf')
        telefone = request.POST.get('telefone')
        sexo = request.POST.get('sexo')
        cep = request.POST.get('cep')
        estado = request.POST.get('estado')
        bairro = request.POST.get('bairro')
        numero = request.POST.get('numero')
        complemento = request.POST.get('complemento')
        
        client = Client(
            user=request.user,  
            cpf=cpf,
            telefone=telefone,
            sexo=sexo,
            cep=cep,
            estado=estado,
            bairro=bairro,
            numero=numero,
            complemento=complemento
        )
        client.save()
        
        messages.success(request, 'Dados complementares cadastrados com sucesso')
        return redirect('register_client_info')
    
    estados_choices = Client._meta.get_field('estado').choices
    sexo_choices = Client._meta.get_field('sexo').choices
    context = {
        'estados_choices': estados_choices,
        'sexo_choices': sexo_choices
    }
    return render(request, 'register_client_info.html', context)

def listar_editar_usuario(request):
    try:
        client = Client.objects.get(user=request.user)
        user = request.user
    except Client.DoesNotExist:
        messages.error(request, 'Cliente não encontrado.')
        return redirect('register_client_info')

    if request.method == 'POST':
        client_form = ClientForm(request.POST, instance=client)
        user_form = UserForm(request.POST, instance=user)

        if client_form.is_valid() and user_form.is_valid():
            client_form.save()
            user_form.save()
            messages.success(request, 'Dados atualizados com sucesso!')
            return redirect('listar_editar_usuario')
    else:
        client_form = ClientForm(instance=client)
        user_form = UserForm(instance=user)

    context = {
        'client_form': client_form,
        'user_form': user_form,
        'client': client
    }
    return render(request, 'listar_usuario.html', context)


@login_required
def listar_pets(request):
    try:
        client = Client.objects.get(user=request.user)
        pets = Animal.objects.filter(client=client, ativo=True)
    except Client.DoesNotExist:
        messages.error(request, 'Cliente não encontrado.')
        return redirect('inicio')

    context = {
        'pets': pets,
    }
    return render(request, 'list_pets.html', context)


@login_required
def edit_pet(request, pet_id):
    try:
        client = Client.objects.get(user=request.user)
    except Client.DoesNotExist:
        messages.error(request, 'Cliente não encontrado.')
        return redirect('inicio')

    animal = get_object_or_404(Animal, id=pet_id, client=client)

    if request.method == 'POST':
        pet_form = AnimalForm(request.POST, instance=animal)

        if pet_form.is_valid():
            pet_form.save()
            messages.success(request, 'Dados do pet atualizados com sucesso!')
            return redirect('listar_pets')
    else:
        pet_form = AnimalForm(instance=animal)

    context = {
        'pet_form': pet_form,
    }
    return render(request, 'edit_pet.html', context)

@login_required
def delete_pet(request, pet_id):
    try:
        client = Client.objects.get(user=request.user)
    except Client.DoesNotExist:
        messages.error(request, 'Cliente não encontrado.')
        return redirect('inicio')

    animal = get_object_or_404(Animal, id=pet_id, client=client)

    if request.method == 'POST':
        if Agendamento.objects.filter(id_animal=animal).exists():            
            animal.ativo = False
            animal.save()
            messages.success(request, 'Pet inativado com sucesso!')
        else:
            animal.delete()
            messages.success(request, 'Pet apagado com sucesso!')
        return redirect('listar_pets')

    context = {
        'animal': animal,
    }
    return render(request, 'delete_pet.html', context)
