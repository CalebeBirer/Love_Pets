from django.urls import path
from . import views

urlpatterns = [
    path('criar_agenda/', views.agendar_servico , name='criar_agenda'),
    path('criar_servico/', views.criar_servico , name='criar_servico'),
    path('meus_agendamentos/', views.listar_agendamentos, name='listar_agendamentos'),
    path('detalhe_agendamento/<int:agendamento_id>/', views.detalhe_agendamento, name='detalhe_agendamento'),
]