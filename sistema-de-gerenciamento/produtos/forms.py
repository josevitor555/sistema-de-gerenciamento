from django import forms
from .models import Produto, Categoria
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario 
from .models import Produto, Categoria, Usuario

'''class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ('nome', 'descricao', 'marca')'''



'''class ProdutoForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), empty_label="Selecione uma Categoria")

    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'marca', 'categoria', 'quantidade', 'valor', 'imagem', 'adicional']'''

from django import forms
from .models import Produto, Categoria

class ProdutoForm(forms.ModelForm):
    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # pode trocar por SelectMultiple se quiser dropdown
        required=True
    )
    
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'marca', 'categorias', 'quantidade', 'valor', 'imagem', 'adicional']

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)



class RegisterForm(forms.Form):
    email = forms.CharField(max_length=255)
    nome = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)

    # Método de validação para garantir que o e-mail não está em uso
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("E-mail já cadastrado.")
        return email


class PesquisaForm(forms.Form):
    query = forms.CharField(label='Pesquisa', max_length=100)



class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome']  # Só nome, pois o model Categoria só tem esse campo



