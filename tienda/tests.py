from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Categoria, Producto, Pedido, ItemPedido


class AgregarAlCarritoTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='ana', password='ClaveSegura#2024')
        self.client.force_login(self.user)
        categoria, _ = Categoria.objects.get_or_create(nombre='Dragon Ball')
        self.producto = Producto.objects.create(
            nombre='Goku', precio=100, stock=10, categoria=categoria
        )

    def test_agregar_crea_carrito_y_item(self):
        url = reverse('tienda_api:agregar_carrito')
        response = self.client.post(url, {'producto_id': self.producto.id, 'cantidad': 2}, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Pedido.objects.filter(usuario=self.user, estado=Pedido.CARRITO).count(), 1)
        self.assertEqual(ItemPedido.objects.get().cantidad, 2)

    def test_agregar_el_mismo_producto_dos_veces_suma_cantidad(self):
        url = reverse('tienda_api:agregar_carrito')
        self.client.post(url, {'producto_id': self.producto.id, 'cantidad': 2}, format='json')
        self.client.post(url, {'producto_id': self.producto.id, 'cantidad': 3}, format='json')

        self.assertEqual(ItemPedido.objects.count(), 1)
        self.assertEqual(ItemPedido.objects.get().cantidad, 5)

    def test_agregar_producto_inexistente_da_400(self):
        url = reverse('tienda_api:agregar_carrito')
        response = self.client.post(url, {'producto_id': 9999, 'cantidad': 1}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ConfirmarCompraTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='ana', password='ClaveSegura#2024')
        self.client.force_login(self.user)
        categoria, _ = Categoria.objects.get_or_create(nombre='Naruto')
        self.producto = Producto.objects.create(
            nombre='Naruto Sabio', precio=150, stock=3, categoria=categoria
        )

    def test_confirmar_con_stock_suficiente_descuenta_stock(self):
        self.client.post(
            reverse('tienda_api:agregar_carrito'),
            {'producto_id': self.producto.id, 'cantidad': 2},
            format='json'
        )
        response = self.client.post(reverse('tienda_api:confirmar_compra'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 1)  # 3 - 2

        pedido = Pedido.objects.get(usuario=self.user)
        self.assertEqual(pedido.estado, Pedido.CONFIRMADO)

    def test_confirmar_sin_stock_suficiente_rechaza_y_no_descuenta(self):
        self.client.post(
            reverse('tienda_api:agregar_carrito'),
            {'producto_id': self.producto.id, 'cantidad': 10},  # solo hay 3
            format='json'
        )
        response = self.client.post(reverse('tienda_api:confirmar_compra'))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 3)
        pedido = Pedido.objects.get(usuario=self.user)
        self.assertEqual(pedido.estado, Pedido.CARRITO)

    def test_confirmar_carrito_vacio_da_400(self):
        response = self.client.post(reverse('tienda_api:confirmar_compra'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CarritoAislamientoTests(APITestCase):
    def setUp(self):
        self.ana = User.objects.create_user(username='ana', password='ClaveSegura#2024')
        self.luis = User.objects.create_user(username='luis', password='ClaveSegura#2024')
        categoria, _ = Categoria.objects.get_or_create(nombre='One Piece')
        self.producto = Producto.objects.create(
            nombre='Luffy', precio=80, stock=5, categoria=categoria
        )

        self.client.force_login(self.ana)
        self.client.post(
            reverse('tienda_api:agregar_carrito'),
            {'producto_id': self.producto.id, 'cantidad': 1},
            format='json'
        )

    def test_el_carrito_de_luis_no_ve_items_de_ana(self):
        self.client.force_login(self.luis)
        response = self.client.get(reverse('tienda_api:carrito'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['items'], [])


class ProductoDetailTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='ana', password='ClaveSegura#2024')
        self.client.force_login(self.user)

    def test_producto_inexistente_da_404(self):
        url = reverse('tienda_api:producto_detail', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
