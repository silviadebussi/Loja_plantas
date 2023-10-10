from django.contrib import admin
from .models import Cliente, Endereco, Pedido, Fisica,Juridica, Categorias, Especie, Status, Planta, HistoricoStatus, models, ItemPedido
from . import models

class ItemPedidoInline(admin.TabularInline):
    model = models.ItemPedido
    extra = 1

class PedidoAdmin(admin.ModelAdmin):
    inlines = [
        ItemPedidoInline
    ]




admin.site.register([Cliente])

admin.site.register(Fisica)

admin.site.register(Juridica)

admin.site.register(Endereco)

admin.site.register(Categorias)

admin.site.register(models.Pedido, PedidoAdmin)

admin.site.register(models.ItemPedido)

admin.site.register(Planta)

admin.site.register(Especie)

admin.site.register(Status)

admin.site.register(HistoricoStatus)

# Register your models here.
