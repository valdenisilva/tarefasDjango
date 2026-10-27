# Encontro 9: models históricos e atualização das tarefas anteriores para uma conta escolhida. Em banco novo vazio, não há dados a atribuir.
import os
from django.conf import settings
from django.db import migrations

def atribuir(apps, schema_editor):
    Tarefa = apps.get_model('tarefas', 'Tarefa')
    banco = schema_editor.connection.alias
    antigas = Tarefa.objects.using(banco).filter(responsavel__isnull=True)
    if not antigas.exists():
        return
    nome = os.environ.get('TAREFAS_USUARIO_LEGADO', '')
    Usuario = apps.get_model(*settings.AUTH_USER_MODEL.split('.'))
    usuario = Usuario.objects.using(banco).filter(username=nome).first()
    if usuario is None:
        raise RuntimeError('Defina TAREFAS_USUARIO_LEGADO com o username de um usuário existente antes de migrar.')
    antigas.update(responsavel_id=usuario.pk)

class Migration(migrations.Migration):
    dependencies = [('tarefas', '0002_responsavel_opcional')]
    operations = [migrations.RunPython(atribuir, migrations.RunPython.noop)]
