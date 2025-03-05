from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Usuario(AbstractUser):
    email = models.EmailField(_("endereço de email"), blank=False)

    def get_absolute_url(self):
        return reverse("ver_perfil", kwargs={"username": self.username})


class Topico(models.Model):
    topico = models.CharField(_("tópico"), max_length=200)
    data_pub = models.DateTimeField(_("data de publicação"), auto_now_add=True)
    slug = models.SlugField(default="", null=False, unique=False)

    class Meta:
        verbose_name = "tópico"

    def __str__(self) -> str:
        if len(self.topico) > 35:
            return self.topico[:35] + "..."
        return self.topico

    def get_absolute_url(self):
        return reverse("entradas", kwargs={"topico": self.slug})


class Entrada(models.Model):
    topico = models.ForeignKey(Topico, on_delete=models.CASCADE)
    texto_entrada = models.TextField(_("entrada"))
    data_pub = models.DateTimeField(_("data de publicação"), auto_now_add=True)
    data_edicao = models.DateTimeField(_("data de edição"), auto_now=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="entradas")

    def __str__(self) -> str:
        return self.texto_entrada

    def get_absolute_url(self):
        topico = self.topico.slug
        return reverse("ver_entrada", kwargs={"pk": self.pk, "topico": topico})