"""Testes para as views de CRUD do modelo `Usuario`"""

from django.test import TestCase
from django.urls import reverse

from diario.models import Usuario, Topico, Entrada


class TestUsuarioCreate(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("criar_conta")
        cls.dados_validos = {
            "username": "usuario",
            "email": "email@teste.com",
            "password1": "123dasilva4",
            "password2": "123dasilva4",
        }
        # senhas diferentes
        cls.dados_invalidos = {
            "username": "usuario",
            "email": "email@teste.com",
            "password1": "123dasilva4",
            "password2": "maisoumenosdesouza",
        }

    def test_criar_usuario_valido(self):
        """Testa criar um usuário com dados válidos"""
        resposta = self.client.post(self.url, self.dados_validos)
        usuario = Usuario.objects.get(username="usuario")

        self.assertIsNotNone(usuario)
        self.assertEqual(self.client.session["_auth_user_id"], str(usuario.pk))
        self.assertRedirects(resposta, reverse("topicos"))

    def test_criar_usuario_invalido(self):
        """Testa criar um usuário com dados inválidos (senhas diferentes)"""
        resposta = self.client.post(self.url, self.dados_invalidos)

        self.assertFormError(
            resposta.context["form"],
            "password2",
            "Os dois campos de senha não correspondem.",
        )

    def test_criar_usuario_email_vazio(self):
        """Testa criar um usuário com campo de email vazio"""
        dados = {
            "username": "usuario",
            "email": "",  # eita
            "password1": "123dasilva4",
            "password2": "123dasilva4",
        }
        resposta = self.client.post(self.url, dados)

        self.assertFormError(
            resposta.context["form"], "email", "Este campo é obrigatório."
        )

    def test_criar_usuario_email_invalido(self):
        """Testa criar um usuário com campo de email inválido"""
        dados = {
            "username": "usuario",
            "email": "veja só o email da lenda",
            "password1": "123dasilva4",
            "password2": "123dasilva4",
        }
        resposta = self.client.post(self.url, dados)

        self.assertFormError(
            resposta.context["form"], "email", "Informe um endereço de email válido."
        )


class TestUsuarioDelete(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(
            username="usuario", email="email@teste.com", password="123456"
        )

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("apagar_conta")

    def test_apagar_usuario_nao_autenticado(self):
        resposta = self.client.get(self.url)
        url_redirect = f"/accounts/login/?next={self.url}"

        self.assertRedirects(resposta, url_redirect)

    def test_apagar_usuario(self):
        self.client.force_login(user=self.usuario)

        resposta = self.client.get(self.url)
        self.assertEqual(resposta.status_code, 200)

        resposta = self.client.post(self.url)
        with self.assertRaises(Usuario.DoesNotExist):
            Usuario.objects.get(username="usuario")


class TestPerfil(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = Usuario.objects.create(
            username="usuario", email="email@teste.com", password="123456"
        )
        cls.outro_usuario = usuario = Usuario.objects.create(
            username="outro", email="abc@teste.com", password="123456"
        )
        cls.topico = Topico.objects.create(topico="Django", slug="django")

        cls.usuario.entradas.create(texto_entrada="entrada 1", topico=cls.topico)
        cls.usuario.entradas.create(texto_entrada="entrada 2", topico=cls.topico)

    def test_ver_perfil(self):
        resposta = self.client.get(self.usuario.get_absolute_url())

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("usuario", resposta.context)
        self.assertEqual(resposta.context["usuario"], self.usuario)
        self.assertIn("entradas", resposta.context)
        self.assertEqual(len(resposta.context["entradas"]), 2)

    def test_ver_perfil_inexistente(self):
        resposta = self.client.get(reverse("ver_perfil", kwargs={"username": "a"}))

        self.assertEqual(resposta.status_code, 404)

    def test_ver_outro_perfil_autenticado(self):
        self.client.force_login(user=self.usuario)
        resposta = self.client.get(self.outro_usuario.get_absolute_url())

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("usuario", resposta.context)
        self.assertEqual(resposta.context["usuario"], self.outro_usuario)

    def test_ver_outro_perfil_nao_autenticado(self):
        resposta = self.client.get(self.outro_usuario.get_absolute_url())

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("usuario", resposta.context)
        self.assertEqual(resposta.context["usuario"], self.outro_usuario)
