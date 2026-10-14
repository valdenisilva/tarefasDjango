# from django.db import models

# # Create your models here.
# # from django.db import models 
# class Categoria(models.Model): 
#     nome = models.CharField(max_length=100) 
#     def __str__(self): 
#         return self.nome 
#     class Tarefa(models.Model): 
#         class Prioridade(models.TextChoices): 
#             BAIXA = "BAIXA", "Baixa" 
#             MEDIA = "MEDIA", "Média" 
#             ALTA = "ALTA", "Alta" 
#     class Situacao(models.TextChoices): 
#         PENDENTE = "PENDENTE", "Pendente" 
#         CONCLUIDA = "CONCLUIDA", "Concluída" 
#     # Material acadêmico • gerado a partir do Markdown 
#     # Semana 7 — Modelagem e Persistência com Django 
#     titulo = models.CharField(max_length=150) 
#     descricao = models.TextField(blank=True) 
#     prioridade = models.CharField( 
#         max_length=10, 
#         choices=Prioridade.choices, 
#         default=Prioridade.MEDIA, 
#     ) 
#     data_prevista = models.DateField() 
#     situacao = models.CharField( 
#         max_length=10, 
#         choices=Situacao.choices, 
#         default=Situacao.PENDENTE, 
#     ) 
#     categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT) 
#     def __str__(self): 
#         return self.titulo 
from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Tarefa(models.Model):
    class Prioridade(models.TextChoices):
        BAIXA = "BAIXA", "Baixa"
        MEDIA = "MEDIA", "Média"
        ALTA = "ALTA", "Alta"

    class Situacao(models.TextChoices):
        PENDENTE = "PENDENTE", "Pendente"
        CONCLUIDA = "CONCLUIDA", "Concluída"

    titulo = models.CharField(max_length=150)
    descricao = models.TextField(blank=True)
    prioridade = models.CharField(
        max_length=10,
        choices=Prioridade.choices,
        default=Prioridade.MEDIA,
    )
    data_prevista = models.DateField()
    situacao = models.CharField(
        max_length=10,
        choices=Situacao.choices,
        default=Situacao.PENDENTE,
    )
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)

    def __str__(self):
        return self.titulo
