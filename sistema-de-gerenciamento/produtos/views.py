from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ProdutoForm,  LoginForm, RegisterForm, PesquisaForm
from .models import Produto, Pedido, ItemPedido, Categoria
from django.contrib import messages
from .models import Usuario
from django.core.paginator import Paginator
from .forms import RegisterForm
from .forms import CategoriaForm
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import ProdutoCategoria
from django.contrib.auth.hashers import make_password
import os
from django.http import JsonResponse
import logging
logger = logging.getLogger(__name__)

from rest_framework import generics
from rest_framework import filters
from .models import Categoria, Produto
from .serializers import CategoriaSerializer, ProdutoSerializer

class CategoriaListAPIView(generics.ListAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProdutoListAPIView(generics.ListAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'descricao', 'marca']
    ordering_fields = ['nome', 'valor', 'updated_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        categori_id = self.request.query_params.get('categoria')
        if categori_id:
            try:
                categori_id = int(categori_id)
                queryset = queryset.filter(categorias__id=categori_id)
            except ValueError:
                # Lida com o caso em que o ID da categoria não é um número válido
                pass
        return queryset


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)  # opcional
        email = request.POST.get('email')
        nome = request.POST.get('nome')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        # Validações simples
        if not nome:
            messages.error(request, "O campo nome é obrigatório.")
            return render(request, 'produtos/login.html', {
                'form': form,
                'is_register': True,
                'email_value': email
            })

        if password != password_confirm:
            messages.error(request, "As senhas não conferem.")
            return render(request, 'produtos/login.html', {
                'form': form,
                'is_register': True,
                'email_value': email
            })

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, "E-mail já está em uso.")
            return render(request, 'produtos/login.html', {
                'form': form,
                'is_register': True,
                'email_value': email
            })

        # Cria o usuário com senha criptografada
        usuario = Usuario(email=email, nome=nome)
        usuario.set_password(password)
        usuario.save()

        messages.success(request, "Cadastro realizado com sucesso!")
        return redirect('login')

    else:
        form = RegisterForm()

    return render(request, 'produtos/login.html', {'form': form, 'is_register': True})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Autenticação com backend personalizado por email
        usuario = authenticate(request, email=email, password=password)

        if usuario is not None:
            login(request, usuario)
            return redirect('produto_list')
        else:
            messages.error(request, "Email ou senha inválidos.")
            return render(request, 'produtos/login.html', {
                'is_register': False,
                'email_value': email
            })

    return render(request, 'produtos/login.html', {'is_register': False})
def logout_view(request):
    logout(request)
    return redirect('login')

def produto_create_view(request):
    # Garante que as categorias iniciais existam
    if not Categoria.objects.exists():
        Categoria.create_initial_categories()

    categorias = Categoria.objects.all()

    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        marca = request.POST.get('marca')
        categoria_nome = request.POST.get('categoria')  # campo vindo do input HTML
        quantidade = request.POST.get('quantidade')
        valor = request.POST.get('valor')
        imagem = request.FILES.get('imagem')
        adicional = request.POST.get('adicional')

        if not nome or not categoria_nome or not valor:
            messages.error(request, 'Preencha todos os campos obrigatórios.')
            return render(request, 'produtos/cadastro.html', {
                'categorias': categorias,
                'form_submetido': True
            })

        try:
            valor = float(valor)
        except ValueError:
            messages.error(request, 'O campo valor deve ser um número válido.')
            return render(request, 'produtos/cadastro.html', {
                'categorias': categorias,
                'form_submetido': True
            })

        categoria, _ = Categoria.get_or_create_categoria(categoria_nome)

        # Primeiro cria o produto sem as categorias
        produto = Produto.objects.create(
            nome=nome,
            descricao=descricao,
            marca=marca,
            quantidade=int(quantidade) if quantidade else 1,
            valor=valor,
            imagem=imagem,
            adicional=adicional
        )

        # Depois associa a categoria com o ManyToManyField
        ProdutoCategoria.objects.create(produto=produto, categoria=categoria)


        messages.success(request, 'Produto cadastrado com sucesso!')
        return render(request, 'produtos/cadastro.html', {
            'categorias': categorias,
            'form_submetido': True
        })

    return render(request, 'produtos/cadastro.html', {
        'categorias': categorias,
        'form_submetido': False
    })
def produto_list_view(request):
    adicional = request.GET.get('adicional')
    categoria = request.GET.get('categoria')

    produtos_list = Produto.objects.all().order_by('-updated_at')

    if adicional:
        produtos_list = produtos_list.filter(adicional=adicional)

    if categoria:
        produtos_list = produtos_list.filter(categorias__nome=categoria)

    paginator = Paginator(produtos_list, 10)
    page_number = request.GET.get('page')
    produtos = paginator.get_page(page_number)

    categorias = Categoria.objects.all()

    return render(request, 'produtos/produto.html', {
        'produtos': produtos,
        'adicional': adicional,
        'categoria_selecionada': categoria,
        'categorias': categorias,
        'mostrar_mensagem': True  # ✅ Só aqui a mensagem será exibida
    })

def produto_search_view(request):
    form = PesquisaForm()
    resultados = []

    if 'query' in request.GET:
        form = PesquisaForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            resultados = Produto.objects.filter(nome__icontains=query)

    return render(request, 'produtos/pesquisa.html', {'form': form, 'resultados': resultados})

def produto_delete_view(request, produto_id):
    produto = Produto.objects.get(id=produto_id)
    if request.method == 'POST':
        produto.delete()
        messages.success(request, 'Produto removido com sucesso!')
        return redirect('produto_list')
    return render(request, 'produtos/confirmar_exclusao.html', {'produto': produto})

def produto_update_view(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        marca = request.POST.get('marca')
        categoria_id = request.POST.get('categoria')  # ID da nova categoria selecionada
        quantidade = request.POST.get('quantidade')
        valor = request.POST.get('valor')
        imagem = request.FILES.get('imagem')
        adicional = request.POST.get('adicional')

        if not valor or not valor.replace('.', '', 1).isdigit():
            messages.error(request, 'O campo valor é obrigatório e deve ser um número.')
            return render(request, 'produtos/editar_produto.html', {
                'produto': produto,
                'categorias': categorias
            })

        # ✅ Atualiza os dados do produto
        produto.nome = nome
        produto.descricao = descricao
        produto.marca = marca
        produto.quantidade = int(quantidade) if quantidade else 0
        produto.valor = float(valor)
        produto.adicional = adicional

        if imagem:
            produto.imagem = imagem

        produto.save()

        # ✅ Atualiza a categoria ManyToMany com modelo intermediário
        ProdutoCategoria.objects.filter(produto=produto).delete()  # Remove todas categorias antigas
        if categoria_id:
            nova_categoria = Categoria.objects.get(id=categoria_id)
            ProdutoCategoria.objects.create(produto=produto, categoria=nova_categoria)

        messages.success(request, 'Produto atualizado com sucesso!')
        return redirect('produto_list')

    return render(request, 'produtos/editar_produto.html', {
        'produto': produto,
        'categorias': categorias
    })


def pedido_list_view(request):
    pedidos = Pedido.objects.all()
    return render(request, 'produtos/lista.html', {'pedidos': pedidos})

def pedido_update_view(request, item_pedido_id, action):
    item_pedido = ItemPedido.objects.get(id=item_pedido_id)
    if action == 'increment':
        item_pedido.quantidade += 1
    elif action == 'decrement' and item_pedido.quantidade > 1:
        item_pedido.quantidade -= 1
    item_pedido.save()
    return redirect('pedido_create')

def pedido_create_view(request):
    produtos = Produto.objects.all()
    if 'pedido_id' in request.session:
        pedido_id = request.session['pedido_id']
        pedido = Pedido.objects.get(id=pedido_id)
    else:
        pedido = Pedido.objects.create()
        request.session['pedido_id'] = pedido.id

    if request.method == 'POST':
        produto_id = request.POST.get('produto')
        quantidade = request.POST.get('quantidade')

        if not quantidade or not quantidade.isdigit():
            messages.error(request, 'O campo quantidade é obrigatório e deve ser um número.')
            return render(request, 'produtos/pedido.html', {'produtos': produtos, 'pedido': pedido})

        produto = Produto.objects.get(id=produto_id)
        item_pedido, created = ItemPedido.objects.get_or_create(pedido=pedido, produto=produto)
        item_pedido.quantidade += int(quantidade)
        item_pedido.save()
        messages.success(request, 'Item adicionado ao pedido com sucesso!')
        return redirect('pedido_create')

    return render(request, 'produtos/pedido.html', {'produtos': produtos, 'pedido': pedido})

def minha_tela_base(request):
    categorias = Categoria.objects.all()
    produtos = Produto.objects.all()
    context = {
        'categorias': categorias,
        'produtos': produtos,
    }
    return render(request, 'base.html', context)

def minha_pagina(request):
    return render(request, 'pagina.html')



# LISTAGEM
def categoria_list_view(request):
    categorias = Categoria.objects.all()
    return render(request, 'produtos/categoria_list.html', {'categorias': categorias})




def categoria_create_view(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            nova_categoria = form.save()
            return JsonResponse({'id': nova_categoria.id, 'nome': nova_categoria.nome})  # 🔥 Retorna JSON
    return render(request, 'produtos/categoria_create.html', {'form': CategoriaForm()})


# ATUALIZAÇÃO
class CategoriaUpdateView(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'produtos/categoria_update.html'
    success_url = reverse_lazy('categoria_list')

# DELEÇÃO
class CategoriaDeleteView(DeleteView):
    model = Categoria
    template_name = 'produtos/categoria_delete.html'
    success_url = reverse_lazy('categoria_list')

def redefinir_senha(request):
    if request.method == "POST":
        email = request.POST.get("email")
        nova_senha = request.POST.get("new_password")
        confirma_senha = request.POST.get("confirm_password")

        if nova_senha == confirma_senha:
            try:
                usuario = Usuario.objects.get(email=email)
                usuario.password = make_password(nova_senha)
                usuario.save()
                
                return render(request, "produtos/login.html", {"mensagem_sucesso": "Senha redefinida com sucesso! Agora você pode fazer login."})
            except Usuario.DoesNotExist:
                return render(request, "produtos/login.html", {"mensagem_erro": "Email não encontrado!"})
        else:
            return render(request, "produtos/login.html", {"mensagem_erro": "Senhas não coincidem!"})

    return render(request, "produtos/login.html")