from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('login/', views.login, name="login"),
    path('logout', views.logout, name="logout"),    
    path('register_client/', views.register_client, name="register_client")
]
