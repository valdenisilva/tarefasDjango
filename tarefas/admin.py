"""Encontro 7: painel de administração do Django.

O registro já oferece telas para consultar e manter os models.
Usuários comuns não recebem is_staff e não acessam esse painel.
"""
from django.contrib import admin
from .models import Categoria, Tarefa

admin.site.register(Categoria)
admin.site.register(Tarefa)
