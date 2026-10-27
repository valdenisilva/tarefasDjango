"""Verificações de apoio: fluxo CRUD, validação, CSRF e isolamento entre usuários."""
from datetime import date
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.db.models.deletion import ProtectedError
from .models import Categoria, Tarefa

class FluxoTests(TestCase):
    # Cada teste recebe dados novos em um banco de teste, separado do SQLite da aula.
    def setUp(self):
        self.usuario = get_user_model().objects.create_user('ana', password='Senha-aula-837!')
        self.outro = get_user_model().objects.create_user('bruno', password='Senha-aula-928!')
        self.categoria = Categoria.objects.create(nome='Estudos')
        self.dados = {'titulo': 'Revisar ORM', 'descricao': 'Exercícios',
                      'prioridade': 'MEDIA', 'data_prevista': '2026-10-22',
                      'categoria': self.categoria.pk}
        self.tarefa = Tarefa.objects.create(titulo='Tarefa inicial', categoria=self.categoria,
                                           data_prevista=date(2026, 10, 22), responsavel=self.usuario)
        self.client.force_login(self.usuario)

    def test_crud_validacao_e_confirmacao(self):
        self.assertContains(self.client.get('/'), 'Tarefa inicial')
        self.assertEqual(self.client.post(reverse('tarefas:criar'), {}).status_code, 200)
        self.assertEqual(Tarefa.objects.count(), 1)
        self.assertRedirects(self.client.post(reverse('tarefas:criar'), self.dados), '/')
        self.assertEqual(Tarefa.objects.count(), 2)
        url = reverse('tarefas:editar', args=[self.tarefa.pk])
        resposta = self.client.get(url)
        self.assertContains(resposta, 'Tarefa inicial')
        self.assertContains(resposta, '2026-10-22')
        self.client.post(url, {**self.dados, 'titulo': 'Alterada'})
        self.tarefa.refresh_from_db()
        self.assertEqual(self.tarefa.titulo, 'Alterada')
        self.assertEqual(Tarefa.objects.count(), 2)
        concluir = reverse('tarefas:concluir', args=[self.tarefa.pk])
        self.assertEqual(self.client.get(concluir).status_code, 405)
        self.client.post(concluir)
        self.tarefa.refresh_from_db()
        self.assertEqual(self.tarefa.situacao, 'CONCLUIDA')
        self.assertEqual(self.tarefa.prioridade, 'MEDIA')
        excluir = reverse('tarefas:excluir', args=[self.tarefa.pk])
        self.assertEqual(self.client.get(excluir).status_code, 200)
        self.assertTrue(Tarefa.objects.filter(pk=self.tarefa.pk).exists())
        self.client.post(excluir)
        self.assertFalse(Tarefa.objects.filter(pk=self.tarefa.pk).exists())

    def test_categoria_protegida_e_404(self):
        with self.assertRaises(ProtectedError):
            self.categoria.delete()
        self.assertEqual(self.client.get('/99999/editar/').status_code, 404)

    def test_csrf(self):
        cliente = Client(enforce_csrf_checks=True)
        cliente.force_login(self.usuario)
        self.assertEqual(cliente.post(reverse('tarefas:criar'), self.dados).status_code, 403)

    def test_isolamento_e_filtros(self):
        alheia = Tarefa.objects.create(titulo='Privada do Bruno', categoria=self.categoria,
                                     data_prevista=date.today(), responsavel=self.outro)
        self.assertNotContains(self.client.get('/'), alheia.titulo)
        for acao in ('editar', 'concluir', 'excluir'):
            url = reverse('tarefas:' + acao, args=[alheia.pk])
            self.assertEqual(self.client.post(url, self.dados).status_code, 404)
            if acao != 'concluir':
                self.assertEqual(self.client.get(url).status_code, 404)
        alheia.refresh_from_db()
        self.assertEqual(alheia.situacao, 'PENDENTE')
        self.assertNotContains(self.client.get('/?situacao=CONCLUIDA'), self.tarefa.titulo)
        self.assertContains(self.client.get('/?categoria=' + str(self.categoria.pk)), self.tarefa.titulo)
        self.assertEqual(self.client.get('/?categoria=invalida&situacao=erro').status_code, 200)
        self.client.post(reverse('tarefas:criar'), {**self.dados, 'responsavel': self.outro.pk, 'situacao': 'CONCLUIDA'})
        nova = Tarefa.objects.latest('pk')
        self.assertEqual(nova.responsavel, self.usuario)
        self.assertEqual(nova.situacao, 'PENDENTE')
        self.assertContains(self.client.get('/'), 'Tarefa cadastrada.')

    def test_login_logout_e_protecao(self):
        self.client.logout()
        for url in ('/', '/nova/', f'/{self.tarefa.pk}/editar/', f'/{self.tarefa.pk}/excluir/'):
            self.assertEqual(self.client.get(url).status_code, 302)
        self.assertEqual(self.client.post(f'/{self.tarefa.pk}/concluir/').status_code, 302)
        self.assertContains(self.client.get('/contas/login/'), 'Entrar')
        self.assertEqual(self.client.post('/contas/login/', {'username': 'ana', 'password': 'errada'}).status_code, 200)
        self.assertRedirects(self.client.post('/contas/login/', {'username': 'ana', 'password': 'Senha-aula-837!'}), '/')
        self.assertEqual(self.client.get('/contas/logout/').status_code, 405)
        self.assertRedirects(self.client.post('/contas/logout/'), '/contas/login/')

    def test_metodos_http_nao_previstos(self):
        # Um método inesperado não pode executar ações que a tela não oferece.
        self.assertEqual(self.client.post('/').status_code, 405)
        self.assertEqual(self.client.put('/nova/').status_code, 405)
        self.assertEqual(self.client.delete(f'/{self.tarefa.pk}/excluir/').status_code, 405)
        self.assertTrue(Tarefa.objects.filter(pk=self.tarefa.pk).exists())

    def test_csrf_aceita_formulario_com_token(self):
        # O teste anterior recusa um POST sem token. Este envia o token correto.
        cliente = Client(enforce_csrf_checks=True)
        cliente.force_login(self.usuario)
        cliente.get('/nova/')
        token = cliente.cookies['csrftoken'].value
        resposta = cliente.post('/nova/', {**self.dados, 'csrfmiddlewaretoken': token})
        self.assertEqual(resposta.status_code, 302)
        self.assertEqual(Tarefa.objects.filter(responsavel=self.usuario).count(), 2)
