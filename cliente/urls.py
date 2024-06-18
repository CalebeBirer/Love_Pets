from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('login/', views.login, name="login"),
    path('logout', views.logout, name="logout"),    
    path('register_client/', views.register_client, name="register_client"),
    path('register_client_info/', views.register_client_info, name='register_client_info'),
    path('register_pet/', views.register_pet, name="register_pet"),
    path('listar_pets/', views.listar_pets, name='listar_pets'),
    path('edit_pet/<int:pet_id>/', views.edit_pet, name='edit_pet'),
    path('listar_editar_usuario/', views.listar_editar_usuario, name='listar_editar_usuario'),
]
