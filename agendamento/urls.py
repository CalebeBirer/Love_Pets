from django.urls import path
from . import views

urlpatterns = [
    path('criar_agenda/', views.agendar_servico , name='criar_agenda'),
    path('criar_servico/', views.criar_servico , name='criar_servico'),
    path('listar_agendamentos/', views.listar_agendamentos, name='listar_agendamentos'),
    path('finalizar_agendamentos/', views.finalizar_agendamentos, name='finalizar_agendamentos'),
]
