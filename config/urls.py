"""Rotas do projeto: Admin, app de tarefas e autenticação nativa."""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    # include delega as rotas de tarefas ao arquivo do próprio app.
    path('', include('tarefas.urls')),
    # LoginView busca templates/registration/login.html por convenção.
    path('contas/login/', auth_views.LoginView.as_view(), name='login'),
    # O Django 5.2 exige POST para logout.
    path('contas/logout/', auth_views.LogoutView.as_view(), name='logout'),
]
