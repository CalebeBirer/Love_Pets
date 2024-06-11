from django.db import models
from cliente.models import Users, Animal

class Servico(models.Model):
    nome = models.CharField(max_length=30)
    descricao = models.CharField(max_length=150, blank=True, null=True)
    duracao = models.DurationField()

    def __str__(self):
        return self.nome

class Agendamento(models.Model):
    data = models.DateField()
    horario = models.TimeField()
    observacao = models.CharField(max_length=150, blank=True, null=True)
    finalizado = models.BooleanField(default=False)
    id_animal = models.ForeignKey(Animal, on_delete=models.PROTECT)
    id_cliente = models.ForeignKey(Users, on_delete=models.PROTECT)
    id_servico = models.ForeignKey(Servico, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.data} {self.horario} - {self.id_servico.nome}"
