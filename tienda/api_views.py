from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Producto, Pedido, ItemPedido
from .serializers import ProductoSerializer, PedidoSerializer, AgregarAlCarritoSerializer


class ProductoDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, producto_id):
        """
        Devuelve el detalle de un producto.

        Si no existe, responde 404 con {"error": <mensaje>}.
        Si existe, responde 200 con ProductoSerializer(producto).data.
        """
        ### START CODE HERE ###
        try:
            producto = Producto.objects.get(pk=producto_id)
        except Producto.DoesNotExist:
            return Response(
                {"error": "Producto no encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(ProductoSerializer(producto).data, status=status.HTTP_200_OK)
        ### END CODE HERE ###


class CarritoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        carrito, _ = Pedido.objects.get_or_create(usuario=request.user, estado=Pedido.CARRITO)
        return Response(PedidoSerializer(carrito).data, status=status.HTTP_200_OK)


class AgregarAlCarritoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Agrega un producto al carrito activo del usuario (Pedido en
        estado 'carrito'), o suma la cantidad si el producto ya estaba.

        Body esperado: {"producto_id": <int>, "cantidad": <int>}
        Responde 201 con PedidoSerializer(carrito).data, o 400 si el
        body es invalido.
        """
        ### START CODE HERE ###
        serializer = AgregarAlCarritoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        producto_id = serializer.validated_data['producto_id']
        cantidad = serializer.validated_data['cantidad']
        producto = Producto.objects.get(pk=producto_id)

        carrito, _ = Pedido.objects.get_or_create(
            usuario=request.user,
            estado=Pedido.CARRITO,
        )

        item = ItemPedido.objects.filter(pedido=carrito, producto=producto).first()
        if item:
            item.cantidad += cantidad
            item.save()
        else:
            ItemPedido.objects.create(
                pedido=carrito,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=producto.precio,
            )

        return Response(PedidoSerializer(carrito).data, status=status.HTTP_201_CREATED)
        ### END CODE HERE ###


class ConfirmarCompraAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Confirma la compra del carrito activo del usuario.

        Valida el stock de todos los items ANTES de modificar nada; si
        alguno no alcanza, responde 400 sin tocar stock. Si todos
        alcanzan, descuenta el stock de cada producto, marca el pedido
        como confirmado, y responde 200 con
        PedidoSerializer(carrito).data.
        """
        ### START CODE HERE ###
        try:
            carrito = Pedido.objects.get(
                usuario=request.user,
                estado=Pedido.CARRITO,
            )
        except Pedido.DoesNotExist:
            return Response(
                {"error": "No hay un carrito activo."},
                status=status.HTTP_404_NOT_FOUND,
            )

        items = list(carrito.items.select_related('producto'))
        if not items:
            return Response(
                {"error": "El carrito está vacío."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        for item in items:
            if item.cantidad > item.producto.stock:
                return Response(
                    {"error": "Stock insuficiente para uno o más productos."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        with transaction.atomic():
            for item in items:
                producto = item.producto
                producto.stock -= item.cantidad
                producto.save()
            carrito.estado = Pedido.CONFIRMADO
            carrito.save()

        return Response(PedidoSerializer(carrito).data, status=status.HTTP_200_OK)
        ### END CODE HERE ###
