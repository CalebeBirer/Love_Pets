from django.urls import path
from .views import agenda_view

urlpatterns = [
    path('criar_agenda/', agenda_view, name='agenda'),
]
