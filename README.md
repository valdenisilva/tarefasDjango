# Gestão de tarefas com Django — projeto comentado

Aplicativo completo para os conteúdos dos encontros 7, 8 e 9 de Laboratório de Programação Back End. Os comentários relacionam o código à teoria. O projeto usa Python 3.12, Django 5.2.18, SQLite, views baseadas em funções, ModelForm e templates nativos.

## Início

Siga **ROTEIRO_DO_ALUNO.md** nesta pasta. Ele apresenta preparação, instalação local, criação do banco e dos usuários, execução e conferência de cada operação.

Este pacote é a versão final integrada. Todos os campos, inclusive responsável, já estão implementados. Os comentários indicam em qual encontro cada conceito aparece. Não confunda esta pasta com as fotografias progressivas `encontro_07`, `encontro_08` e `encontro_09` entregues anteriormente.

## Funcionalidades

- Login e logout nativos do Django.
- Listagem das tarefas do usuário autenticado.
- Cadastro e edição com validação e exibição de erros.
- Conclusão somente por POST.
- Exclusão somente após confirmação por POST.
- Filtros por situação e categoria.
- Mensagens de sucesso após operações.
- Categorias compartilhadas, administradas exclusivamente pelo Admin.
- Autorização por responsável em todas as operações por identificador.

## Onde a teoria aparece

| Conteúdo | Arquivo principal |
|---|---|
| Models, campos, escolhas e relacionamentos | `tarefas/models.py` |
| Histórico da estrutura e migração de dados | `tarefas/migrations/` |
| Consultas ORM, filtros e atualização | `tarefas/views.py` e prática do roteiro |
| Painel administrativo | `tarefas/admin.py` |
| Rotas, parâmetros e namespace | `tarefas/urls.py`, `config/urls.py` |
| Contexto e ciclo requisição-resposta | `tarefas/views.py` |
| Herança, repetição e estado vazio | `templates/base.html`, `templates/tarefas/lista.html` |
| ModelForm, campos explícitos e widgets | `tarefas/forms.py` |
| Cadastro e edição com instance | `tarefas/views.py`, `templates/tarefas/form.html` |
| Conclusão e exclusão confirmada | Views e `templates/tarefas/confirmar_exclusao.html` |
| Login, logout, sessão e redirecionamento | `config/urls.py`, `config/settings.py`, `templates/registration/login.html` |
| Autorização e responsável automático | `tarefas/views.py` |
| Mensagens após redirecionar | Views e template base |
| Arquivos estáticos | `tarefas/static/tarefas/estilo.css` |

## Estrutura

```text
gestao_tarefas/
  README.md
  ROTEIRO_DO_ALUNO.md
  VALIDACAO.md
  requirements.txt
  .gitignore
  manage.py
  config/
    __init__.py
    settings.py
    urls.py
    wsgi.py
  tarefas/
    __init__.py
    models.py
    forms.py
    views.py
    urls.py
    admin.py
    tests.py
    migrations/
      __init__.py
      0001_initial.py
      0002_responsavel_opcional.py
      0003_atribuir_responsavel.py
      0004_responsavel_obrigatorio.py
    static/tarefas/estilo.css
  templates/
    base.html
    registration/login.html
    tarefas/lista.html
    tarefas/form.html
    tarefas/confirmar_exclusao.html
```

O banco `db.sqlite3` e a pasta `.venv` surgem no computador de cada aluno. O pacote não contém contas, senhas ou banco preenchido. `VALIDACAO.md` diferencia verificações executadas de atividades a realizar em sala.

## Decisões didáticas

`PROTECT` impede excluir categorias com tarefas. `CASCADE` remove as tarefas quando o administrador exclui seu responsável. A descrição é opcional. A situação inicial é PENDENTE. O formulário não permite escolher responsável nem situação. Não há regra que proíba datas passadas. Categorias não possuem CRUD público e não há cadastro público de usuários.

A execução descrita é **local, para a aula**. `DEBUG=True` e a chave fixa de laboratório não representam uma configuração para publicar na internet.
