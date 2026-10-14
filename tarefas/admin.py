from django.contrib import admin

# Register your models here.
# from django.contrib import admin
from .models import Categoria, Tarefa

admin.site.register(Categoria)
admin.site.register(Tarefa)
