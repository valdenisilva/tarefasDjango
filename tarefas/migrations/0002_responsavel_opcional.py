# Encontro 9: campo opcional temporário permite migrar linhas existentes.
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('tarefas', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [migrations.AddField(
        model_name='tarefa', name='responsavel',
        field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                to=settings.AUTH_USER_MODEL, verbose_name='responsável'),
    )]
