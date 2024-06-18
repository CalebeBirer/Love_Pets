from django import forms
from django.contrib.auth import forms as auth_forms  
from .models import Users, Client

class UserChangeForm(auth_forms.UserChangeForm):
    class Meta(auth_forms.UserChangeForm.Meta):
        model = Users

class UserCreationForm(auth_forms.UserCreationForm):
    class Meta(auth_forms.UserCreationForm.Meta):
        model = Users

class UserForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email']

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['cpf', 'telefone', 'sexo', 'cep', 'estado', 'bairro', 'numero', 'complemento']