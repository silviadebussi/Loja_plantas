from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms
from .models import Endereco, AvaliacaoCategoria, Compra
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'hello'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'hi',
        }
))
    

class EnderecoForm(forms.Form):
    rua = forms.CharField(label='Rua', max_length=100)
    cidade = forms.CharField(label='Cidade', max_length=50)
    estado = forms.CharField(label='Estado', max_length=50)
    numero = forms.CharField(label='Número', max_length=10)
    cep = forms.CharField(label='CEP', max_length=10)

    def __init__(self, user, *args, **kwargs):
        super(EnderecoForm, self).__init__(*args, **kwargs)
        self.user = user

class AvaliacaoCategoriaForm(forms.ModelForm):
    class Meta:
        model = AvaliacaoCategoria
        fields = ['categoria', 'avaliacao', 'comentario']
        widgets = {
            'comentario': forms.Textarea(attrs={'rows': 4}),
        }
class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['endereco', 'cliente', 'metodo_pagamento']  

class AvaliacaoCategoriaForm(forms.ModelForm):
    class Meta:
        model = AvaliacaoCategoria
        fields = ['avaliacao', 'comentario']