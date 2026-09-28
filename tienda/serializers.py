from rest_framework import serializers
from .models import Categoria, Producto, Pedido, ItemPedido


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']


class ProductoSerializer(serializers.ModelSerializer):
    ### START CODE HERE ###
    categoria = CategoriaSerializer(read_only=True)

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'stock', 'imagen', 'categoria']
    ### END CODE HERE ###


class ProductoMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'imagen']


class ItemPedidoSerializer(serializers.ModelSerializer):
    producto = ProductoMiniSerializer(read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = ItemPedido
        fields = ['id', 'producto', 'cantidad', 'precio_unitario', 'subtotal']


class PedidoSerializer(serializers.ModelSerializer):
    items = ItemPedidoSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Pedido
        fields = ['id', 'estado', 'creado_en', 'items', 'total']


class AgregarAlCarritoSerializer(serializers.Serializer):
    ### START CODE HERE ###
    producto_id = serializers.IntegerField()
    cantidad = serializers.IntegerField(min_value=1)

    def validate_producto_id(self, value):
        if not Producto.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Producto no encontrado.")
        return value
    ### END CODE HERE ###
