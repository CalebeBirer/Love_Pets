from django import forms
from .models import Agendamento

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['data', 'horario', 'observacao', 'id_animal', 'id_servico']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'horario': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'observacao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite as Observações...'}),
            'id_animal': forms.Select(attrs={'class': 'form-control'}),
            'id_servico': forms.Select(attrs={'class': 'form-control'}),
        }
