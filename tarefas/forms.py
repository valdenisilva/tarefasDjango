"""Encontro 8: ModelForm reutiliza a validação declarada no model."""
from django import forms
from .models import Tarefa


class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        # Lista explícita: situação e responsável não podem vir do navegador.
        # A situação muda na ação concluir. O responsável vem de request.user.
        fields = ['titulo', 'descricao', 'prioridade', 'data_prevista', 'categoria']
        widgets = {
            # O input HTML date espera ano-mês-dia no atributo value.
            # Esse formato também mantém a data preenchida ao editar.
            'data_prevista': forms.DateInput(
                format='%Y-%m-%d', attrs={'type': 'date'},
            ),
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }
