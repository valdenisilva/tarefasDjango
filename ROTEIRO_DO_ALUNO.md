# Roteiro do aluno — implantação local e estudo do projeto

## Resultado esperado

Ao concluir este roteiro, você terá o aplicativo funcionando no navegador, com duas contas comuns, categorias e tarefas persistidas no SQLite. Você também terá verificado o CRUD, os filtros e o bloqueio de acesso entre usuários.

Neste material, **implantar significa preparar e executar no seu computador**, usando o servidor de desenvolvimento do Django. O roteiro não exige nuvem ou conta paga.

## 1. Preparação do computador

Você precisa de Windows, Python 3.12, um editor de código e navegador. Git será usado apenas para registrar a entrega. Abra o PowerShell e confira:

```powershell
py -3.12 --version
```

Resultado esperado: `Python 3.12.x`. Se o comando não encontrar o Python, instale essa versão antes de prosseguir. O projeto fixa Django 5.2.18 em `requirements.txt`.

Extraia o ZIP. Abra a pasta `gestao_tarefas` no editor e abra um terminal nela. O comando abaixo precisa mostrar `manage.py`:

```powershell
Get-ChildItem
```

**Ponto de conferência:** você está na pasta que contém `manage.py`, `requirements.txt`, `config` e `tarefas`. Todos os comandos seguintes partem dela, salvo indicação contrária.

## 2. Ambiente virtual e dependência

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m django --version
```

Resultado esperado no último comando: `5.2.18`.

O ambiente virtual separa as dependências deste trabalho das de outros projetos. Usaremos diretamente seu executável Python, sem precisar ativá-lo. Isso evita problemas com a política de execução de scripts do PowerShell.

**Ponto de conferência:** a pasta `.venv` existe e a versão do Django aparece sem erro. A instalação da dependência requer acesso à internet.

Não execute `startproject` nem `startapp`: o pacote já contém o projeto `config` e o app `tarefas`.

## 3. Leitura das configurações

Abra `config/settings.py` e localize:

- `INSTALLED_APPS`: inclui `tarefas` e os recursos nativos de autenticação, Admin, sessões, mensagens e arquivos estáticos.
- `MIDDLEWARE`: inclui sessão, CSRF, autenticação e mensagens.
- `TEMPLATES`: procura os arquivos na pasta `templates` e fornece `request`, `user` e `messages` ao HTML.
- `DATABASES`: aponta para `db.sqlite3` na pasta do projeto.
- `LANGUAGE_CODE` e `TIME_ZONE`: definem português e o fuso de São Paulo.
- `LOGIN_URL`, `LOGIN_REDIRECT_URL` e `LOGOUT_REDIRECT_URL`: usam os nomes das rotas de entrada e saída.

**Questão para registrar:** por que incluir o app em `INSTALLED_APPS` é necessário para o Django descobrir seus models?

## 4. Banco de dados novo

Para começar sem dados anteriores:

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py showmigrations tarefas
```

O primeiro comando verifica a configuração. O segundo cria as tabelas. O terceiro deve mostrar as quatro migrações de tarefas com `[X]`.

As migrações já acompanham o pacote. **Não é necessário gerar novamente os arquivos.** Durante o desenvolvimento de uma alteração real no model, a sequência é `makemigrations tarefas` e depois `migrate`.

A primeira migração cria Categoria e Tarefa. As seguintes introduzem o responsável de forma gradual para aceitar também bancos antigos. No banco novo vazio, não há tarefa antiga para atribuir e nenhuma variável de usuário legado é necessária.

**Ponto de conferência:** existe `db.sqlite3` e todas as migrações de tarefas estão aplicadas.

Se você está trazendo um banco do encontro 8, use o procedimento específico da seção 17 antes de continuar. Não sobreponha bancos diferentes.

## 5. Superusuário e servidor

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

Escolha um nome, por exemplo `professor`, e uma senha local. A digitação da senha não aparece no terminal. Guarde a senha para a aula sem incluí-la no código ou no relatório.

Inicie o servidor:

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

Mantenha esse terminal aberto. Acesse:

- Aplicativo: http://127.0.0.1:8000/
- Administração: http://127.0.0.1:8000/admin/

O aplicativo direciona visitantes para o login. O Admin exige conta com permissão de equipe, como o superusuário recém-criado.

**Ponto de conferência:** você consegue entrar no Admin. Para outros comandos, abra um segundo terminal na mesma pasta. Para parar o servidor, use Ctrl+C.

## 6. Categorias e contas comuns

No Admin:

1. Em Categorias, cadastre `Estudos` e `Pessoal`.
2. Em Usuários, adicione `ana` e defina uma senha escolhida por você.
3. Crie também `bruno`, com outra senha.
4. Nas permissões de Ana e Bruno, mantenha as contas ativas e deixe desmarcados os campos de membro da equipe e superusuário. Elas não precisam de permissões de models para usar as páginas de tarefas.

Categorias são compartilhadas. Sua manutenção acontece pelo Admin. Os usuários comuns não precisam acessar esse painel.

**Ponto de conferência:** existem duas categorias e duas contas comuns, além do superusuário.

## 7. Primeiro acesso e cadastro

Saia do Admin. Abra o aplicativo e entre como Ana.

Cadastre:

| Campo | Tarefa 1 | Tarefa 2 |
|---|---|---|
| Título | Revisar ORM | Organizar agenda |
| Descrição | Refazer as consultas da aula | Pode ficar vazia |
| Prioridade | Média | Baixa |
| Data prevista | Uma data escolhida por você | Uma data escolhida por você |
| Categoria | Estudos | Pessoal |

Você não escolhe situação nem responsável. A nova tarefa começa PENDENTE e a view define Ana como responsável.

**Ponto de conferência:** duas tarefas aparecem na lista e o cadastro apresenta uma mensagem de sucesso.

## 8. Models, relacionamento e persistência — encontro 7

Abra `tarefas/models.py`. Leia os comentários de Categoria e Tarefa.

Identifique:

1. Um campo de texto curto e seu limite de tamanho.
2. O campo opcional e o significado de `blank=True`.
3. O campo de data.
4. Os valores persistidos e os rótulos de prioridade e situação.
5. A ForeignKey de categoria e a ação `PROTECT`.
6. O método `__str__` de cada model.

O campo responsável faz parte da versão final, mas seu conceito pertence ao encontro 9. A modelagem inicial do encontro 7 não tinha esse vínculo.

Pare o servidor, inicie novamente e atualize a listagem. Entre novamente se necessário.

**Ponto de conferência:** as tarefas continuam disponíveis. Os dados ficam no SQLite, não apenas na memória do servidor.

## 9. Consultas e atualização com ORM — encontro 7

No segundo terminal:

```powershell
.\.venv\Scripts\python.exe manage.py shell
```

Execute os blocos abaixo no shell Python:

```python
from django.contrib.auth import get_user_model
from tarefas.models import Categoria, Tarefa

ana = get_user_model().objects.get(username='ana')
Categoria.objects.all()
Tarefa.objects.all()
Tarefa.objects.filter(responsavel=ana, situacao='PENDENTE')
Tarefa.objects.filter(responsavel=ana, categoria__nome='Estudos')
Tarefa.objects.filter(responsavel=ana).order_by('data_prevista')
```

`all()` consulta o conjunto completo. `filter()` restringe registros. `order_by()` ordena. Os dois sublinhados em `categoria__nome` permitem consultar um campo do model relacionado.

O shell é uma ferramenta administrativa: ele não passa pelas views e pode consultar todos os usuários. O isolamento da interface é implementado nas views.

Atualize uma tarefa pendente:

```python
tarefa = Tarefa.objects.filter(responsavel=ana, situacao='PENDENTE').first()
if tarefa is not None:
    tarefa.situacao = Tarefa.Situacao.CONCLUIDA
    tarefa.save(update_fields=['situacao'])
    tarefa.refresh_from_db()
    print(tarefa.pk, tarefa.titulo, tarefa.get_situacao_display())
else:
    print('Cadastre uma tarefa pendente antes de continuar.')
```

Finalize o bloco com uma linha vazia no shell. `first()` pode retornar `None`; por isso verificamos o resultado. `refresh_from_db()` relê os valores persistidos.

Saia com `exit()` e confira a situação na listagem.

**Ponto de conferência:** uma consulta filtrada e uma atualização funcionaram. Registre as saídas no relatório.

## 10. Caminho da requisição e templates — encontro 8

Com o aplicativo aberto, acompanhe uma visita à listagem:

1. `config/urls.py` delega ao app com `include`.
2. `tarefas/urls.py` associa a rota à função `lista`.
3. `tarefas/views.py` consulta o banco e monta o contexto.
4. `templates/tarefas/lista.html` percorre as tarefas.
5. `templates/base.html` fornece estrutura, navegação e CSS.

Localize no código:

- `app_name = 'tarefas'` e uma rota com `<int:pk>`.
- `{% url 'tarefas:lista' %}` e um link de edição que recebe `tarefa.pk`.
- `{% extends 'base.html' %}` e `{% block content %}`.
- `{% for ... %}`, `{% empty %}` e a apresentação de rótulos com `get_situacao_display`.
- O filtro de data `date:"d/m/Y"`.
- `{% load static %}` e o caminho do stylesheet.

**Questão para registrar:** o que a chave `'tarefas'` do contexto permite fazer no template?

## 11. Formulário, validação e edição — encontro 8

Abra `tarefas/forms.py`. A classe TarefaForm herda de ModelForm e declara os campos permitidos em `Meta.fields`. O widget de data usa o formato esperado pelo input HTML.

Na view `criar`:

- GET cria um formulário sem dados enviados.
- POST cria um formulário vinculado a `request.POST`.
- `is_valid()` verifica os dados antes de persistir.
- A resposta inválida renderiza o mesmo formulário, preservando dados e erros.
- A resposta válida salva e redireciona para a listagem.

Na view `editar`, `instance=tarefa` informa qual registro atualizar. A mesma página `form.html` atende cadastro e edição, com títulos diferentes.

Pratique:

1. Abra Nova tarefa, preencha os demais campos e deixe o título vazio. O navegador pode impedir o envio pela validação HTML.
2. Para conferir a validação **do servidor**, execute o teste automatizado da seção 15, que envia o POST inválido diretamente. Não remova o token CSRF.
3. Edite o título ou prioridade de uma tarefa existente.
4. Confira que a data aparece preenchida e que a quantidade de tarefas não aumentou.

**Ponto de conferência:** entrada inválida não cria registro. Edição mantém o ID da tarefa. TarefaForm não expõe responsável nem situação.

## 12. Conclusão e exclusão — encontro 8

1. Clique em Concluir numa tarefa pendente. A tarefa continua na lista, com situação Concluída.
2. Abra a URL de conclusão diretamente na barra do navegador, por exemplo `/1/concluir/`, usando um ID seu. A resposta esperada é **405**, porque GET não deve alterar a tarefa.
3. Clique em Excluir. A aplicação mostra título, Cancelar e Confirmar exclusão.
4. Cancele e confira que a tarefa permanece.
5. Repita com uma tarefa de teste e confirme a exclusão.

Localize `@require_POST`, `update_fields=['situacao']` e o ramo `if request.method == 'POST'` da exclusão.

GET apresenta a confirmação. Somente o POST remove o registro. Os formulários POST incluem `{% csrf_token %}`. Os decoradores de método também recusam verbos inesperados, como DELETE direto na rota de exclusão.

**Ponto de conferência:** concluir altera apenas a situação. Abrir a confirmação ou cancelar não exclui.

## 13. Login e autorização — encontro 9

Abra `config/urls.py` e localize LoginView e LogoutView. Depois confira as configurações de redirecionamento e `templates/registration/login.html`.

Autenticação identifica a pessoa. Autorização define o que ela pode acessar.

Nas views:

- `@login_required` exige sessão autenticada.
- A listagem começa com `filter(responsavel=request.user)`.
- Edição, conclusão e exclusão buscam `pk` e `responsavel=request.user` juntos.
- No cadastro, `form.save(commit=False)` cria o objeto sem gravar, e a view atribui o responsável antes de `save()`.

Faça o teste com duas contas:

1. Como Ana, cadastre uma tarefa e copie sua URL de edição.
2. Use Sair. O botão envia um POST para encerrar a sessão.
3. Entre como Bruno. A tarefa de Ana não deve aparecer.
4. Cole a URL de edição de Ana. O resultado esperado é **404**, mesmo sabendo o ID.
5. Cadastre uma tarefa como Bruno, saia e volte como Ana. Ela também não deve ver a tarefa dele.
6. Saia e tente abrir a listagem. Você deve seguir para o login.

O teste automatizado também envia POSTs para tarefas alheias, cobrindo conclusão e exclusão. Ocultar botões não seria suficiente para proteger os dados.

**Ponto de conferência:** nenhum usuário comum mantém tarefas de outra pessoa.

## 14. Mensagens e filtros — encontro 9

Faça um cadastro, uma edição e uma conclusão. Em cada operação, observe o aviso após o redirecionamento. No código, relacione `messages.success()` da view ao laço `for message in messages` do template base.

Depois:

1. Filtre tarefas pendentes.
2. Filtre tarefas concluídas.
3. Combine uma situação com a categoria Estudos.
4. Use Limpar.
5. Confira a URL com os parâmetros de consulta.

O formulário de filtros usa GET, pois apenas consulta. A view valida os valores e aplica os filtros ao conjunto já restrito ao usuário. Situação ou categoria inválida é ignorada, sem falha do servidor.

**Ponto de conferência:** filtro nunca mostra tarefa alheia e um resultado vazio apresenta mensagem compreensível.

## 15. Verificações automáticas de apoio

No terminal da pasta do projeto:

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe manage.py test tarefas
```

Resultados esperados: nenhuma inconsistência, nenhuma mudança pendente e testes com `OK`. O Django usa um banco de testes separado. As contas e tarefas criadas nos testes não substituem as contas que você criou para a demonstração.

Os testes ajudam a verificar autorização, CSRF e POST inválido. Nesta aula, concentre-se em entender os fluxos. O aprofundamento de testes e refatoração pode continuar no encontro 10.

## 16. Registro e entrega

Se esta pasta ainda não pertence a um repositório e o professor solicitar Git, execute `git init`. Em seguida:

```powershell
git status
git add .
git commit -m "Implementa gestão de tarefas com autenticação e comentários didáticos"
```

Revise a lista de arquivos antes do commit. `.gitignore` exclui ambiente virtual, caches e banco local. Os arquivos de migração devem aparecer na entrega. Não inclua senhas.

Entregue o código e um registro curto com:

```text
Aluno ou dupla:
Versão do Python e Django:
Operações verificadas:
Resultado esperado e observado:
Consulta ORM executada:
Dificuldade encontrada e solução:
Verificações ainda pendentes:
```

Checklist final:

- [ ] Instalei e executei o projeto localmente.
- [ ] Criei duas categorias e duas contas comuns.
- [ ] Cadastrei pelo menos duas tarefas.
- [ ] Conferi persistência depois de reiniciar o servidor.
- [ ] Executei consulta filtrada e atualização pelo ORM.
- [ ] Entendi o caminho entre URL, view, contexto e template.
- [ ] Validei cadastro, edição, conclusão e exclusão confirmada.
- [ ] Testei login e logout.
- [ ] Conferi que dois usuários não acessam tarefas um do outro.
- [ ] Testei filtros e mensagens.
- [ ] Executei os testes de apoio e registrei o resultado.
- [ ] Registrei uma dificuldade e sua solução.

## 17. Caminho opcional: reaproveitar um banco do encontro 8

Esta seção serve **somente** para quem já tem o banco com Categoria e Tarefa, mas ainda sem responsável. Quem começou com banco novo pela seção 4 não precisa executá-la.

1. Pare o servidor antigo e o novo.
2. Faça uma cópia de segurança do banco antigo. Não copie arquivos enquanto houver gravações em andamento.
3. Trabalhe em uma cópia do projeto com os mesmos models e histórico inicial. O roteiro pressupõe a migração `tarefas/0001_initial.py` do material anterior. Se seu histórico for diferente, compare-o com o professor antes de aplicar este procedimento.
4. Preserve o banco antigo na pasta desta versão **sem sobrescrever um banco de destino existente**. Não apague migrações e não use `--fake` para forçar a atualização.
5. Instale as dependências da nova pasta e execute:

```powershell
.\.venv\Scripts\python.exe manage.py migrate tarefas 0002
```

Se ainda não existe a conta que receberá as tarefas antigas, crie-a agora:

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

Escolha uma conta existente ou a recém-criada e informe seu username. Exemplo com `professor`:

```powershell
$env:TAREFAS_USUARIO_LEGADO = "professor"
.\.venv\Scripts\python.exe manage.py migrate
Remove-Item Env:TAREFAS_USUARIO_LEGADO
```

`0002` adiciona o campo temporariamente opcional. `0003` atribui as tarefas sem responsável à conta escolhida. `0004` torna a relação obrigatória. Se a conta não existir, a migração para com uma mensagem: ajuste a conta ou variável e repita `migrate`.

Todas as tarefas antigas passam ao usuário escolhido. O sistema não tem informação para deduzir quem as criou anteriormente. Os demais campos permanecem. A migração de dados não desfaz essa atribuição ao reverter, portanto preserve a cópia de segurança.

Confira com `showmigrations tarefas`, abra o aplicativo com a conta escolhida e compare quantidade, título, categoria e data com o banco anterior.

## 18. Erros e formas de conferir

| Sintoma | Ação |
|---|---|
| Python não encontrado | Conferir instalação e `py -3.12 --version` |
| `No module named django` | Instalar requirements usando o Python de `.venv` |
| `can't open file manage.py` | Entrar na pasta correta |
| `no such table` | Rodar migrate nessa mesma pasta |
| Categoria não aparece no formulário | Cadastrar categorias pelo Admin |
| `TemplateDoesNotExist` | Conferir nome, caminho e configuração TEMPLATES |
| `NoReverseMatch` | Conferir namespace `tarefas` e nome da rota |
| 403 em formulário | Conferir CSRF e cookies. Não desabilitar a proteção |
| 405 em concluir ou sair pelo navegador | Usar os botões POST da interface |
| 404 ao usar ID de outro usuário | Restrição esperada de autorização |
| Formulário com erro | Ler as mensagens junto aos campos e corrigir os valores |
| Dados parecem desaparecer | Conferir qual pasta contém o SQLite em uso |
| Categoria não pode ser excluída | Ela ainda possui tarefas e usa PROTECT |
| Porta 8000 em uso | Parar o outro servidor ou usar `manage.py runserver 8001` e abrir a porta 8001 |
| Migração solicita usuário legado | Seguir a seção 17 com uma conta existente |

## Referências de consulta

- Models: https://docs.djangoproject.com/en/5.2/topics/db/models/
- ORM: https://docs.djangoproject.com/en/5.2/topics/db/queries/
- ModelForm: https://docs.djangoproject.com/en/5.2/topics/forms/modelforms/
- Templates: https://docs.djangoproject.com/en/5.2/topics/templates/
- Autenticação: https://docs.djangoproject.com/en/5.2/topics/auth/default/
- Mensagens: https://docs.djangoproject.com/en/5.2/ref/contrib/messages/

O roteiro acompanha os conteúdos dos encontros 7, 8 e 9 e as atividades hands-on das semanas 7 e 8 fornecidas pelo professor.
