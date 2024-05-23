from django.shortcuts import render
from django.http import HttpResponse
from .models import Users
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

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
            return HttpResponse('Email ja existe')
        
        if (senha != confirma_senha):
            return HttpResponse('Senhas são diferentes')
        
        user = Users.objects.create_user(username=email, 
                                        email=email, 
                                        password=senha, 
                                        first_name=nome, 
                                        last_name=sobrenome,
                                        cargo="C")

        messages.add_message(request, messages.SUCCESS, 'Usuario cadastrado com sucesso')
        return redirect(reverse('register_client'))
