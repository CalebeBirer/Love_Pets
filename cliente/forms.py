from django import forms
from django.contrib.auth import forms as auth_forms  
from .models import Users, Client, Animal

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
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['cpf', 'telefone', 'sexo', 'cep', 'estado', 'cidade', 'bairro', 'numero', 'complemento']
        widgets = {
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'id': 'cpf'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'id': 'telefone'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'id': 'cep'}),
            'estado': forms.Select(attrs={'class': 'form-control', 'id': 'estado'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'id': 'cidade'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control', 'id': 'bairro'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control', 'id': 'complemento'}),
        }

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields['cep'].required = True
        self.fields['complemento'].required = True
        self.fields['cidade'].required = False
        self.fields['estado'].required = False
        self.fields['bairro'].required = False
        self.fields['numero'].required = False


class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['nome', 'raca', 'tipo_pelo', 'porte']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'raca': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_pelo': forms.Select(attrs={'class': 'form-control'}),
            'porte': forms.Select(attrs={'class': 'form-control'}),
        }