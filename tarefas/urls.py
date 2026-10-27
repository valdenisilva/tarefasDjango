"""Encontro 8: cada endereço seleciona uma view baseada em função."""
from django.urls import path
from . import views

# Nos templates, o nome completo será tarefas:lista, tarefas:editar etc.
app_name = 'tarefas'
urlpatterns = [
    path('', views.lista, name='lista'),
    path('nova/', views.criar, name='criar'),
    # O conversor int extrai o identificador e o passa como argumento pk.
    path('<int:pk>/editar/', views.editar, name='editar'),
    path('<int:pk>/concluir/', views.concluir, name='concluir'),
    path('<int:pk>/excluir/', views.excluir, name='excluir'),
]
