from django.shortcuts import render
from django.http import HttpResponse
from .models import Users, Animal
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required

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
        return redirect(reverse('register_client'))

def login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            # redirect redireciona para a pagina desejada e o reverse tranforma o nome em um URL
            return redirect(reverse('register_client')) 
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
    if request.method == "GET":
        return render(request, 'register_pet.html')
    elif request.method == "POST":
        nome_pet = request.POST.get('nome')
        raca = request.POST.get('raca')
        tipo_pelo = request.POST.get('tipo_pelo')
        porte = request.POST.get('porte')
        id_cliente = request.user.id  # Obtém o ID do cliente logado

        animal = Animal(
            nome=nome_pet,
            raca=raca,
            tipo_pelo=tipo_pelo,
            porte=porte,
            id_client=id_cliente
        )
        
        animal.save()

        messages.add_message(request, messages.SUCCESS, 'Pet cadastrado com sucesso')
        return render(request, 'inicio.html')
