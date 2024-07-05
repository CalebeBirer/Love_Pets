from django import forms

class AgendamentoFilterForm(forms.Form):
    data_inicio = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    data_fim = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    status = forms.ChoiceField(choices=[('', 'Todos'), ('Pendente', 'Pendente'), ('Finalizado', 'Finalizado')], required=False, 
                               widget=forms.Select(attrs={'class': 'form-control'}))
