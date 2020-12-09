from django import forms
from .models import Medico, User, MeusPacientes


class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        exclude = ('dados_pessoais', 'data_criacao')


class UserForm(forms.ModelForm):
    senha = forms.CharField(max_length=32, widget=forms.PasswordInput)
    confirmar_senha = forms.CharField(max_length=32, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')


class FormPacientes(forms.ModelForm):
    class Meta:
        model = MeusPacientes
        fields = ('paciente',)

