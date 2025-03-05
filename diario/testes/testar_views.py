"""Testes para as views de CRUD do modelo `Entrada`"""

from django.test import TestCase
from django.urls import reverse

from diario.models import Topico, Entrada, Usuario

from time import sleep


class TestEntradaList(TestCase):
    """Classe para testar a view `EntradaList`"""

    @classmethod
    def setUpTestData(cls):
        cls.usuario = Usuario.objects.create(
            username="usuario", email="usuario@teste.com", password="123456"
        )
        cls.topico = Topico.objects.create(topico="Django", slug="django")
        cls.url = reverse("entradas", kwargs={"topico": cls.topico.slug})

    def test_sem_entradas(self):
        """Testa as respostas da página quando não há entradas"""
        resposta = self.client.get(self.url)
        self.assertContains(resposta, "Não há nenhuma entrada, seja o primeiro!")
        self.assertEqual(resposta.status_code, 200)
        self.assertQuerySetEqual(resposta.context["entradas"], [])

    def test_com_entradas(self):
        """Testa as respostas da página quando há entradas"""
        entrada1 = Entrada.objects.create(
            usuario=self.usuario, topico=self.topico, texto_entrada="oi"
        )
        sleep(0.2)
        entrada2 = Entrada.objects.create(
            usuario=self.usuario, topico=self.topico, texto_entrada="olá"
        )
        resposta = self.client.get(self.url)
        self.assertEqual(resposta.status_code, 200)
        self.assertQuerySetEqual(resposta.context["entradas"], [entrada2, entrada1])


class TestEntradaCreate(TestCase):
    """Classe para testar a view `EntradaCreate`"""

    @classmethod
    def setUpTestData(cls):
        cls.usuario = Usuario.objects.create(
            username="usuario", password="123456", email="usuario@teste.com"
        )
        cls.topico = Topico.objects.create(topico="Django", slug="django")
        cls.url = reverse("criar_entrada", kwargs={"topico": cls.topico.slug})

    def test_criar_entrada_nao_autenticado(self):
        """Testa criar uma entrada com usuário não autenticado"""
        resposta = self.client.get(self.url)
        self.assertRedirects(resposta, f"/accounts/login/?next={self.url}")

    def test_criar_entrada_autenticado(self):
        """Testa criar uma entrada com usuário autenticado"""
        self.client.force_login(user=self.usuario)
        dados = {"texto_entrada": "olha o que eu digitei"}
        resposta = self.client.post(self.url, dados)
        url_redirect = reverse("entradas", kwargs={"topico": self.topico.slug})
        entrada = Entrada.objects.first()
        self.assertEqual(entrada.topico, self.topico)
        self.assertEqual(entrada.usuario, self.usuario)
        self.assertRedirects(resposta, url_redirect)

    def test_create_entrada_invalid(self):
        """Testa o caso de erro de validação (campo vazio ou inválido)"""
        self.client.force_login(user=self.usuario)
        data = {
            "texto_entrada": "",
        }
        resposta = self.client.post(self.url, data)

        self.assertEqual(Entrada.objects.count(), 0)


class TestEntradaDetail(TestCase):
    """Classe para testar a view `EntradaDetail`"""

    @classmethod
    def setUpTestData(cls):
        cls.usuario = Usuario.objects.create(
            username="usuario", password="123456", email="usuario@teste.com"
        )
        cls.topico = Topico.objects.create(topico="Django", slug="django")
        cls.entrada = Entrada.objects.create(
            topico=cls.topico, texto_entrada="oi", usuario=cls.usuario
        )
        cls.url = cls.entrada.get_absolute_url()

    def test_ver_entrada_nao_autenticado(self):
        """Testa ver uma entrada com usuário não autenticado"""
        resposta = self.client.get(self.url)
        self.assertRedirects(resposta, f"/accounts/login/?next={self.url}")

    def test_ver_entrada_autenticado(self):
        """Testa ver uma entrada com usuário autenticado"""
        self.client.force_login(user=self.usuario)
        resposta = self.client.get(self.url)
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, self.entrada.texto_entrada)

    def test_ver_entrada_inexistente(self):
        """Testa ver uma entrada que não existe"""
        self.client.force_login(user=self.usuario)
        resposta = self.client.get(
            reverse("ver_entrada", kwargs={"topico": self.topico.slug, "pk": 9999})
        )
        self.assertEqual(resposta.status_code, 404)


class TestEntradaUpdate(TestCase):
    """Classe para testar a view `EntradaDetail`"""

    @classmethod
    def setUpTestData(cls):
        cls.usuario = Usuario.objects.create(
            username="usuario", password="123456", email="usuario@teste.com"
        )
        cls.topico = Topico.objects.create(topico="Django", slug="django")
        cls.entrada = Entrada.objects.create(
            topico=cls.topico, texto_entrada="oi", usuario=cls.usuario
        )
        cls.url = cls.entrada.get_absolute_url()
        cls.url_editar = reverse(
            "editar_entrada", kwargs={"topico": cls.topico.slug, "pk": cls.entrada.pk}
        )

    def test_editar_entrada_nao_autenticado(self):
        """Testa editar uma entrada com usuário não autenticado"""
        resposta = self.client.get(self.url_editar)
        url_redirect = f"/accounts/login/?next={self.url_editar}"
        self.assertRedirects(resposta, url_redirect)

    def test_editar_entrada_nao_existente(self):
        """Testa editar uma entrada que não existe"""
        self.client.force_login(user=self.usuario)
        url = reverse("editar_entrada", kwargs={"topico": self.topico.slug, "pk": 1234})
        resposta = self.client.get(url)
        self.assertEqual(resposta.status_code, 404)

    def test_editar_entrada(self):
        """Testa editar uma entrada normalmente"""
        entrada = Entrada.objects.create(
            topico=self.topico, usuario=self.usuario, texto_entrada="testando"
        )
        url_redirect = reverse("entradas", kwargs={"topico": self.topico.slug})
        url_edicao = reverse(
            "editar_entrada", kwargs={"topico": entrada.topico.slug, "pk": entrada.pk}
        )

        self.client.force_login(user=self.usuario)
        resposta = self.client.post(url_edicao, {"texto_entrada": "texto atualizado"})

        entrada.refresh_from_db()  # recarrega a entrada
        self.assertEqual(entrada.texto_entrada, "texto atualizado")
        self.assertRedirects(resposta, url_redirect)


class TestEntradaDelete(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = Usuario.objects.create(
            username="usuario", password="123456", email="usuario@teste.com"
        )
        cls.topico = Topico.objects.create(topico="Django", slug="django")
        cls.entrada = Entrada.objects.create(
            topico=cls.topico, texto_entrada="oi", usuario=cls.usuario
        )
        cls.url_apagar = reverse(
            "apagar_entrada", kwargs={"topico": cls.topico.topico, "pk": cls.entrada.pk}
        )

    def test_apagar_entrada_nao_autenticado(self):
        """Testa apagar uma entrada com usuário não autenticado"""
        resposta = self.client.get(self.url_apagar)
        url_redirect = f"/accounts/login/?next={self.url_apagar}"

        self.assertRedirects(resposta, url_redirect)

    def test_apagar_entrada_autenticado(self):
        """Testa apagar uma entrada com usuário autenticado"""
        self.client.force_login(user=self.usuario)
        resposta = self.client.post(self.url_apagar)

        self.assertFalse(Entrada.objects.filter(pk=self.entrada.pk).exists())

    def test_apagar_entrada_inexistente(self):
        """Testa apagar uma entrada inexistente"""
        self.client.force_login(user=self.usuario)
        url = reverse(
            "apagar_entrada", kwargs={"topico": self.topico.topico, "pk": 999}
        )
        resposta = self.client.post(url)

        self.assertEqual(resposta.status_code, 404)
