from django.contrib import admin
from .models import Cliente, Endereco, Pedido, ItemPedido, Fisica,Juridica, Categorias, Especie, Status, Planta, HistoricoStatus

admin.site.register([Cliente])

admin.site.register(Fisica)

admin.site.register(Juridica)

admin.site.register(Endereco)

admin.site.register(Pedido)

admin.site.register(ItemPedido)

admin.site.register(Categorias)

admin.site.register(Planta)

admin.site.register(Especie)

admin.site.register(Status)

admin.site.register(HistoricoStatus)
# Register your models here.
