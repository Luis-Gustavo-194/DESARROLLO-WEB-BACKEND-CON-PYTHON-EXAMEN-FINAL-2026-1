from django.urls import path
from . import api_views

app_name = 'tienda_api'

urlpatterns = [
    path('productos/<int:producto_id>/', api_views.ProductoDetailAPIView.as_view(), name='producto_detail'),
    path('carrito/', api_views.CarritoAPIView.as_view(), name='carrito'),
    path('carrito/agregar/', api_views.AgregarAlCarritoAPIView.as_view(), name='agregar_carrito'),
    path('carrito/confirmar/', api_views.ConfirmarCompraAPIView.as_view(), name='confirmar_compra'),
]
