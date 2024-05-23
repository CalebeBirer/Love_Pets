from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('loign/', views.login, name="login"),
    path('register_client/', views.register_client, name="register_client")
]
