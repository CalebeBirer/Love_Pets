from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    choices_cargo = (('W', 'Owner'), ('C', 'Client'))
    cargo = models.CharField(max_length=1, choices=choices_cargo)
    is_active = models.BooleanField(default=False) 

class Client(models.Model):
    cpf = models.CharField(max_length=14)
    telefone = models.CharField(max_length=15, blank=False, null=False)
    choices_sexo = (('M', 'Masculino'), ('F', 'Feminino'))
    sexo = models.CharField(max_length=1, choices=choices_sexo)
    cep = models.CharField(max_length=11)
    choices_estado = (
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'),
        ('CE', 'Ceará'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'), ('DF', 'Distrito Federal')
    )
    estado = models.CharField(max_length=2, choices=choices_estado, default='SP', blank=False, null=False)
    cidade = models.CharField(max_length=100, blank=False, null=False)
    bairro = models.CharField(max_length=100, blank=False, null=False)
    numero = models.CharField(max_length=10, blank=False, null=False)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    user = models.OneToOneField(Users, on_delete=models.CASCADE)



class Animal(models.Model):
    nome = models.CharField(max_length=50)
    raca = models.CharField(max_length=25)
    choices_pelo = (('L', 'Longo'),
                     ('C', 'Curto'))
    tipo_pelo = models.CharField(max_length=1, choices=choices_pelo, default='C')
    choices_porte = (('P', 'Pequeno'),
                     ('M', 'Medio'),
                     ('G', 'Grande'))
    porte = models.CharField(max_length=1, choices=choices_porte, default='P')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True) 

    def __str__(self):
        return self.nome
