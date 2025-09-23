from django.urls import path
from . import views
from django.shortcuts import redirect
from django.contrib.auth.views import PasswordResetView
from django.urls import path, include
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView,PasswordResetConfirmView



urlpatterns = [
    path('cadastro/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('produtos/', views.produto_list_view, name='produto_list'),
    path('produto_novo/', views.produto_create_view, name='produto_create'),
    path('pesquisa/', views.produto_search_view, name='produto_search'),
    path('produto/excluir/<int:produto_id>/', views.produto_delete_view, name='produto_delete'),
    path('produto/atualizar/<int:produto_id>/', views.produto_update_view, name='produto_update'),  # novo
    path('pedido_novo/', views.pedido_create_view, name='pedido_create'),
    path('pedido_update/<int:item_pedido_id>/<str:action>/', views.pedido_update_view, name='pedido_update'),
    path('pedidos/', views.pedido_list_view, name='pedido_list'),
    path('', lambda request: redirect('login'), name='redirect_login'),
    path('pagina/', views.minha_pagina, name='minha_pagina'),
    path('categorias/', views.categoria_list_view, name='categoria_list'),
    path('categorias/nova/', views.categoria_create_view, name='categoria_create'),
    path('categorias/<int:pk>/editar/', views.CategoriaUpdateView.as_view(), name='categoria_update'),
    path('categorias/<int:pk>/excluir/', views.CategoriaDeleteView.as_view(), name='categoria_delete'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('accounts/', include('allauth.urls')),
    path('auth/', include('social_django.urls', namespace='social')),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),  
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('redefinir_senha/', views.redefinir_senha, name='redefinir_senha'),
    path('', lambda request: redirect('login'), name='redirect_login'),



]







