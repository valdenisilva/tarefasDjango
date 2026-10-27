"""Encontros 8 e 9: requisições, formulários e autorização por responsável.

GET apresenta telas ou consulta dados. POST altera os registros.
Após um POST válido, redirecionamos para evitar repetição ao atualizar a tela.
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from .forms import TarefaForm
from .models import Categoria, Tarefa


@login_required
@require_GET
def lista(request):
    # READ do CRUD. O filtro de responsável vem ANTES dos filtros da tela.
    # Assim, um parâmetro da URL nunca amplia o acesso a tarefas alheias.
    tarefas = Tarefa.objects.filter(responsavel=request.user).order_by(
        'data_prevista', 'pk',
    )
    situacao = request.GET.get('situacao', '')
    categoria = request.GET.get('categoria', '')

    # Só aceitamos os valores previstos nas escolhas do model.
    if situacao in Tarefa.Situacao.values:
        tarefas = tarefas.filter(situacao=situacao)
    else:
        situacao = ''

    # Categorias são compartilhadas, mas apenas o administrador as mantém.
    categorias = Categoria.objects.order_by('nome')
    ids_validos = {str(pk) for pk in categorias.values_list('pk', flat=True)}
    # Texto inválido em categoria não chega ao filtro numérico do banco.
    if categoria in ids_validos:
        tarefas = tarefas.filter(categoria_id=categoria)
    else:
        categoria = ''

    # O contexto dá nome às variáveis que o template poderá usar.
    contexto = {
        'tarefas': tarefas,
        'categorias': categorias,
        'situacoes': Tarefa.Situacao.choices,
        'situacao_atual': situacao,
        'categoria_atual': categoria,
    }
    return render(request, 'tarefas/lista.html', contexto)


@login_required
@require_http_methods(['GET', 'POST'])
def criar(request):
    # GET: formulário vazio. POST: formulário vinculado aos dados enviados.
    form = TarefaForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        # CREATE do CRUD. Precisamos atribuir o dono antes de gravar.
        tarefa = form.save(commit=False)
        tarefa.responsavel = request.user
        tarefa.save()
        messages.success(request, 'Tarefa cadastrada.')
        return redirect('tarefas:lista')

    # Se houve erro, reutilizamos o form vinculado para preservar dados e erros.
    return render(request, 'tarefas/form.html', {
        'form': form, 'titulo': 'Nova tarefa',
    })


@login_required
@require_http_methods(['GET', 'POST'])
def editar(request, pk):
    # Autorização por objeto: conhecer o ID não basta para acessar a tarefa.
    # A mesma busca responde 404 para registro inexistente ou de outro usuário.
    tarefa = get_object_or_404(Tarefa, pk=pk, responsavel=request.user)
    form = TarefaForm(
        request.POST if request.method == 'POST' else None,
        instance=tarefa,  # UPDATE: altera esta linha, sem criar outra tarefa.
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Tarefa atualizada.')
        return redirect('tarefas:lista')
    return render(request, 'tarefas/form.html', {
        'form': form, 'titulo': 'Editar tarefa',
    })


@login_required
@require_POST  # Abrir esta URL com GET não pode alterar dados (retorna 405).
def concluir(request, pk):
    tarefa = get_object_or_404(Tarefa, pk=pk, responsavel=request.user)
    tarefa.situacao = Tarefa.Situacao.CONCLUIDA
    # Atualiza só a situação. Título, prioridade e dono ficam como estavam.
    tarefa.save(update_fields=['situacao'])
    messages.success(request, 'Tarefa concluída.')
    return redirect('tarefas:lista')


@login_required
@require_http_methods(['GET', 'POST'])
def excluir(request, pk):
    tarefa = get_object_or_404(Tarefa, pk=pk, responsavel=request.user)
    if request.method == 'POST':
        # DELETE do CRUD. Só o botão de confirmação envia este POST.
        tarefa.delete()
        messages.success(request, 'Tarefa excluída.')
        return redirect('tarefas:lista')
    # GET apenas apresenta a confirmação, sem remover o registro.
    return render(request, 'tarefas/confirmar_exclusao.html', {'tarefa': tarefa})
