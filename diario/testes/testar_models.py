from django.test import TestCase

from diario.models import Topico, Entrada, Usuario


class UsuarioModelTest(TestCase):
    """Classe para testar o modelo `Usuario`"""

    def test_criacao_usuario(self):
        """Testa a criação básica de usuários com os parâmetros fornecidos"""
        usuario = Usuario.objects.create(
            username="usuario", email="email@teste.com", password="123456"
        )
        self.assertEqual(usuario.username, "usuario")
        self.assertEqual(usuario.email, "email@teste.com")

    def test_usuario_get_absolute_url(self):
        """Testa o método `get_absolute_url()`"""
        usuario = Usuario(
            username="usuario", email="email@teste.com", password="123456"
        )
        self.assertEqual(usuario.get_absolute_url(), "/accounts/perfil/usuario")


class TopicoModelTest(TestCase):
    """Classe para testar o modelo `Topico`"""

    def test_criacao_topico(self):
        """Testa a criação de tópicos com parâmetros fornecidos"""
        topico = Topico.objects.create(topico="Física", slug="fisica")
        self.assertEqual(topico.topico, "Física")
        self.assertEqual(topico.slug, "fisica")

    def test_topico_get_absolute_url(self):
        """Testa o método `get_absolute_url()`"""
        topico = Topico.objects.create(topico="Física", slug="fisica")
        self.assertEqual(topico.get_absolute_url(), "/entradas/fisica")

    def test_topico_str(self):
        """Testa o método `__str__()`"""
        topico1 = Topico.objects.create(
            topico="Este é um tópico bem longo, algum problema com isso?",
            slug="este-e-um-topico-bem-longo-algum-problema-com-isso",
        )
        topico2 = Topico.objects.create(
            topico="Veja aqui o seu tópico", slug="veja-aqui-o-seu-topico"
        )

        self.assertEqual(str(topico1), "Este é um tópico bem longo, algum p...")
        self.assertEqual(str(topico2), "Veja aqui o seu tópico")


class EntradaModelTest(TestCase):
    """Testes para o modelo `Entrada`"""

    @classmethod
    def setUpTestData(cls):
        cls.usuario = Usuario.objects.create(
            username="usuario", email="usuario@teste.com", password="123456"
        )
        cls.topico = Topico.objects.create(topico="Django", slug="django")

    def test_criacao_entrada(self):
        """Testa a criação de entradas com parâmetros fornecidos"""
        entrada = Entrada.objects.create(
            topico=self.topico, usuario=self.usuario, texto_entrada="teste"
        )
        self.assertEqual(entrada.usuario.username, "usuario")
        self.assertEqual(entrada.topico.topico, "Django")
        self.assertEqual(entrada.texto_entrada, "teste")

    def test_entrada_get_absolute_url(self):
        """Testa o método `get_absolute_url()`"""
        entrada2 = Entrada.objects.create(
            topico=self.topico, usuario=self.usuario, texto_entrada="teste"
        )
        self.assertEqual(entrada2.get_absolute_url(), "/entradas/django/ver/1")

    def test_entrada_str(self):
        """Testa o método `__str__()`"""
        entrada = Entrada.objects.create(
            topico=self.topico,
            usuario=self.usuario,
            texto_entrada="Olha só o que eu digitei aqui",
        )
        self.assertEqual(str(entrada), "Olha só o que eu digitei aqui")
