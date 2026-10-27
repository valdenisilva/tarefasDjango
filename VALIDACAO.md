# Verificação da versão comentada

Verificado em 22/10/2026 com Python 3.12.14 e Django 5.2.18.

## Executado

- `manage.py check`: nenhum problema identificado.
- `manage.py makemigrations --check --dry-run`: nenhuma alteração de model sem migração.
- `manage.py test tarefas`: **7 testes aprovados**.

Os testes cobrem cadastro, validação de entrada inválida, edição sem duplicação, data preenchida, conclusão por POST, exclusão confirmada, proteção de categorias, 404, CSRF com token ausente e válido, login e logout, restrição entre dois usuários, filtros, mensagem após cadastro e campos extras que não podem definir situação ou responsável.

Também verificam que métodos HTTP inesperados não executam operações: POST na listagem, PUT no cadastro e DELETE na rota de confirmação recebem 405.

As migrações completas são aplicadas ao banco de teste pelo Django. As migrações de evolução são as mesmas da versão anterior, com comentários adicionais. O teste de migração de um SQLite preenchido do encontro 8 para o encontro 9 foi executado na entrega anterior. Esse cenário não foi repetido nesta revisão, pois as operações de migração não mudaram.

## Atividades para execução pelo aluno

- Instalar em seu ambiente virtual Windows.
- Criar superusuário, categorias e contas comuns pelo Admin.
- Executar o roteiro no navegador e conferir o visual.
- Parar e reiniciar o servidor para conferir a persistência manualmente.
- Registrar evidências e realizar os commits solicitados pelo professor.

Nenhuma conta, senha, banco preenchido ou commit foi incluído na entrega. Os testes renderizam os templates, mas esta revisão não incluiu inspeção visual no navegador nem instalação em outro computador.
