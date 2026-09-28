from django.contrib import admin
from .models import Categoria, Producto, Pedido, ItemPedido


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre']


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'categoria', 'precio', 'stock']
    list_filter = ['categoria']


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'estado', 'total', 'creado_en']
    list_filter = ['estado']
    inlines = [ItemPedidoInline]
