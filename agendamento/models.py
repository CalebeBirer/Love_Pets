from django.db import models
from cliente.models import Users, Animal

class Servico(models.Model):
    """
    Modelo que representa um serviço oferecido.
    """
    nome = models.CharField(max_length=30)
    descricao = models.CharField(max_length=150, blank=True, null=True)
    duracao = models.DurationField()

    def __str__(self):
        return self.nome

class Agendamento(models.Model):
    """
    Modelo que representa um agendamento de serviço para um animal de estimação.
    """
    data = models.DateField()
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    observacao = models.CharField(max_length=150, blank=True, null=True)
    finalizado = models.BooleanField(default=False)
    animal = models.ForeignKey(Animal, on_delete=models.PROTECT)
    cliente = models.ForeignKey(Users, on_delete=models.PROTECT)
    servico = models.ForeignKey(Servico, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.data} {self.horario_inicio} - {self.servico.nome}"
