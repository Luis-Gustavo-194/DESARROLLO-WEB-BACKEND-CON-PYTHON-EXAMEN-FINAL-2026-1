from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    nombre = models.CharField(max_length=64, unique=True)
    descripcion = models.TextField(blank=True, default="")

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=128)
    descripcion = models.TextField(blank=True, default="")
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')

    def __str__(self):
        return f"{self.nombre} (S/ {self.precio})"


class Pedido(models.Model):
    CARRITO = 'carrito'
    CONFIRMADO = 'confirmado'
    ESTADOS = [
        (CARRITO, 'Carrito'),
        (CONFIRMADO, 'Confirmado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos')
    estado = models.CharField(max_length=20, choices=ESTADOS, default=CARRITO)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creado_en']

    @property
    def total(self):
        return sum((item.subtotal for item in self.items.all()), 0)

    def __str__(self):
        return f"Pedido #{self.id} de {self.usuario.username} ({self.estado})"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
