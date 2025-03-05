"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import path, include

from diario import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", views.IndexView.as_view(), name="index"),
    path("topicos/", views.TopicoList.as_view(), name="topicos"),
    path(
        "criar-conta/",
        views.UsuarioCreate.as_view(),
        name="criar_conta"
    ),
    path(
        "accounts/apagar-conta",
        views.UsuarioDelete.as_view(),
        name="apagar_conta"
    ),
    path(
        "accounts/perfil/<str:username>",
        views.Perfil.as_view(),
        name="ver_perfil"
    ),
    path(
        "accounts/alterar-senha",
        PasswordChangeView.as_view(template_name="registration/alterar_senha.html"),
        name="alterar_senha"
    ),
    path(
        "accounts/alterar-senha",
        PasswordChangeDoneView.as_view(template_name="registration/senha_alterada.html"),
        name="alterar_senha"
    ),
    path(
        "entradas/<slug:topico>", views.EntradaList.as_view(), name="entradas"
    ),
    path(
        "entradas/<slug:topico>/criar",
        views.EntradaCreate.as_view(),
        name="criar_entrada"
    ),
    path(
        "entradas/<slug:topico>/ver/<int:pk>",
        views.EntradaDetail.as_view(),
        name="ver_entrada"
    ),
    path(
        "entradas/<slug:topico>/editar/<int:pk>",
        views.EntradaUpdate.as_view(),
        name="editar_entrada"
    ),
    path(
        "entradas/<slug:topico>/apagar/<int:pk>",
        views.EntradaDelete.as_view(),
        name="apagar_entrada"
    ),
]
