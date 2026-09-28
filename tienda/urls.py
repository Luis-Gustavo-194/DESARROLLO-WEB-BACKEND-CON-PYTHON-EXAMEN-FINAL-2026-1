from django.urls import path
from . import views

app_name = 'tienda'

urlpatterns = [
    path('', views.ingreso, name='ingreso'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
]
