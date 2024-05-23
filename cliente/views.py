from django.shortcuts import render
from django.http import HttpResponse
from rolepermissions.decorators  import has_permission_decorator
from .models import Users

def inicio(request):
    return render(request, '../templates/base.html')

def login(request):
    return render(request, '../templates/login.html')

def register_client(request):
    return HttpResponse('Teste')


@has_permission_decorator('cadastrar_vendedor')
def cadastrar_vendedor(request):
    if request.method == "GET":
        vendedores = Users.objects.filter(cargo="V")