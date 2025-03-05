from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from .models import Entrada, Topico, Usuario
from .forms import UsuarioCreationForm


class IndexView(generic.TemplateView):
    template_name = "index.html"


class TopicoList(generic.ListView):
    model = Topico
    template_name = "topicos.html"
    context_object_name = "topicos"

    def get_queryset(self):
        topicos = Topico.objects.annotate(num_entradas=Count("entrada")).order_by("-data_pub")
        return topicos


class EntradaList(generic.ListView):
    model = Entrada
    template_name = "entradas.html"
    context_object_name = "entradas"

    def get_queryset(self):
        topico = get_object_or_404(Topico, slug=self.kwargs["topico"])
        entradas = Entrada.objects.filter(topico=topico).order_by("-data_pub")
        return entradas

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        t = get_object_or_404(Topico, slug=self.kwargs["topico"])
        context["nome_topico"] = t.topico
        context["topico"] = self.kwargs["topico"]
        return context


class EntradaCreate(LoginRequiredMixin, generic.CreateView):
    model = Entrada
    fields = ["texto_entrada"]
    template_name = "criar_entrada.html"

    def get_success_url(self):
        return reverse_lazy("entradas", kwargs={"topico": self.kwargs["topico"]})

    def form_valid(self, form):
        entrada = form.save(commit=False)
        topico = Topico.objects.get(slug=self.kwargs["topico"])
        entrada.topico = topico
        entrada.usuario = self.request.user
        entrada.save()
        return super().form_valid(form)


class EntradaDetail(LoginRequiredMixin, generic.DetailView):
    model = Entrada
    template_name = "ver_entrada.html"
    context_object_name = "entrada"

    def get_object(self, queryset=None):
        return get_object_or_404(Entrada, pk=self.kwargs["pk"])


class EntradaUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Entrada
    template_name = "editar_entrada.html"
    fields = ["texto_entrada"]

    def get_success_url(self):
        return reverse_lazy("entradas", kwargs={"topico": self.kwargs["topico"]})


class EntradaDelete(LoginRequiredMixin, generic.DeleteView):
    model = Entrada

    def get_success_url(self):
        return reverse_lazy("entradas", kwargs={"topico": self.kwargs["topico"]})


class UsuarioCreate(generic.FormView):
    form_class = UsuarioCreationForm
    template_name = "criar_usuario.html"
    success_url = reverse_lazy("topicos")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        redirect(self.get_success_url())
        return super().form_valid(form)


class UsuarioDelete(LoginRequiredMixin, generic.DeleteView):
    model = Usuario
    template_name = "accounts/apagar_conta.html"
    success_url = reverse_lazy("topicos")

    def get_object(self, queryset=None):
        return self.request.user


class UsuarioConfirmarDelete(LoginRequiredMixin, generic.DeleteView):
    template_name = 'accounts/confirmar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class Perfil(generic.DetailView):
    template_name = "accounts/perfil.html"
    model = Usuario
    context_object_name = "usuario"

    def get_object(self, queryset=None):
        username = self.kwargs["username"]
        usuario = get_object_or_404(Usuario, username=username)
        return usuario

    def get_context_data(self, **kwargs):
        usuario = self.get_object()
        context = super().get_context_data(**kwargs)
        context["entradas"] = usuario.entradas.filter()
        return context