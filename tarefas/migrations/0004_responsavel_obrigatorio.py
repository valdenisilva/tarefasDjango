# Encontro 9: após atribuir os registros antigos, o banco passa a exigir responsável.
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [('tarefas', '0003_atribuir_responsavel')]
    operations = [migrations.AlterField(
        model_name='tarefa', name='responsavel',
        field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                to=settings.AUTH_USER_MODEL, verbose_name='responsável'),
    )]
