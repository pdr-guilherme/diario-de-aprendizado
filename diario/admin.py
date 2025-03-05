from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Entrada, Topico, Usuario

# Register your models here.


class TopicoAdmin(admin.ModelAdmin):
    model = Topico
    fields = ["topico", "slug"]
    list_display = ["topico", "data_pub", "slug"]
    list_filter = ["data_pub"]
    prepopulated_fields = {"slug": ["topico"]}


class EntradaAdmin(admin.ModelAdmin):
    model = Entrada
    fields = ["topico", "texto_entrada", "usuario"]
    list_display = ["texto_entrada", "topico", "data_pub", "data_edicao", "usuario"]
    list_filter = ["topico", "data_pub", "data_edicao"]

    def save_model(self, request, obj, form, change):
        if not obj.usuario and request.user.is_authenticated:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Usuario, UserAdmin)
admin.site.register(Topico, TopicoAdmin)
admin.site.register(Entrada, EntradaAdmin)
