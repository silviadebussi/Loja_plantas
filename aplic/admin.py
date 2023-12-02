from django.contrib import admin
from .models import  Cliente, Endereco, Pedido, Categorias, Especie, Status, Planta, HistoricoStatus, models, ItemPedido, AvaliacaoCategoria, Compra
from . import models
from django.utils.html import format_html


class ItemPedidoInline(admin.TabularInline):
    model = models.ItemPedido
    extra = 1

class PedidoAdmin(admin.ModelAdmin):
    inlines = [
        ItemPedidoInline
    ]


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome','cpf', 'user']


@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ['rua', 'numero','complemento', 'bairro', 'cidade', 'cep', 'cliente']
    list_filter = ['estado']

@admin.register(Categorias)
class CategoriasAdmin(admin.ModelAdmin):
    list_display = ['nome', 'manutencao', 'cultivo']

admin.site.register(models.Pedido, PedidoAdmin)

admin.site.register(models.ItemPedido)

class CompraAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'display_itens', 'total', 'data', 'endereco')

    def display_itens(self, obj):
        # Verifica se a compra tem itens associados
        if obj.itens.exists():
            # Se houver, cria uma lista formatada com os nomes dos itens
            itens_list = [str(item) for item in obj.itens.all()]
            return format_html('<br>'.join(itens_list))
        else:
            return "No items"
    
    display_itens.short_description = 'Itens da Compra'



admin.site.register(Compra, CompraAdmin)

@admin.register(Planta)
class PlantaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'get_descricao', 'imagem')

    def get_descricao(self, obj):
        return obj.descricao

    get_descricao.short_description = 'Descrição'

@admin.register(Especie)
class EspecieAdmin(admin.ModelAdmin):
    list_display = ['nome_da_especie','descrição','Categoria_Botânica','Necessidades_de_Luz','Usos_da_Espécie','imagem']

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_filter = ['nome']

@admin.register(HistoricoStatus)
class HistoricoStatusAdmin(admin.ModelAdmin):
    list_display = ['data', 'status']

@admin.register(AvaliacaoCategoria)
class AvaliacaoCategoriaAdmin(admin.ModelAdmin):
    list_display = ['avaliacao','comentario','data']
    list_filter = ['categoria']
