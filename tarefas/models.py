"""Encontro 7: modelagem. Encontro 9: vínculo da tarefa com o usuário.

Models descrevem os registros persistidos. As migrações transformam essas
declarações em tabelas e alterações no banco SQLite.
"""
from django.conf import settings
from django.db import models


class Categoria(models.Model):
    # CharField atende textos curtos. O Django cria a chave primária id.
    nome = models.CharField('nome', max_length=80)

    def __str__(self):
        # Admin, selects de formulário e shell exibem esse texto.
        return self.nome


class Tarefa(models.Model):
    # Cada escolha tem um valor de banco e um rótulo legível na interface.
    class Prioridade(models.TextChoices):
        BAIXA = 'BAIXA', 'Baixa'
        MEDIA = 'MEDIA', 'Média'
        ALTA = 'ALTA', 'Alta'

    class Situacao(models.TextChoices):
        PENDENTE = 'PENDENTE', 'Pendente'
        CONCLUIDA = 'CONCLUIDA', 'Concluída'

    titulo = models.CharField('título', max_length=150)
    # blank=True permite deixar o campo vazio no formulário.
    descricao = models.TextField('descrição', blank=True)
    prioridade = models.CharField(
        'prioridade', max_length=5,
        choices=Prioridade.choices, default=Prioridade.MEDIA,
    )
    # DateField guarda uma data, sem horário. Não há restrição a datas passadas.
    data_prevista = models.DateField('data prevista')
    situacao = models.CharField(
        'situação', max_length=9,
        choices=Situacao.choices, default=Situacao.PENDENTE,
    )
    # Muitas tarefas podem usar a mesma categoria. PROTECT impede remover
    # uma categoria enquanto alguma tarefa ainda depender dela.
    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, verbose_name='categoria',
    )
    # Encontro 9: o usuário vem do Django, sem criar outra tabela de login.
    # Excluir o usuário também exclui suas tarefas (CASCADE).
    # Esse campo não aparece no formulário público: a view atribui o usuário.
    responsavel = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, verbose_name='responsável',
    )

    def __str__(self):
        return self.titulo
