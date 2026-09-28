# AnimeFiguras — examen de backend

Tienda de figuras de anime. La base del proyecto ya está armada y
funcionando (login, registro, catálogo con filtros, la página de detalle
de producto) — tu trabajo es completar **4 piezas del backend** para que
la tienda quede funcional de punta a punta.

## Cómo correrlo

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt

python manage.py migrate       # crea las tablas Y siembra datos de ejemplo
python manage.py runserver
```

La migración ya deja 3 categorías, 6 figuras (una sin stock, a propósito)
y un usuario de prueba:

```
usuario:    demo
contraseña: DemoAnime#2024
```

Ese usuario es `is_staff=True`, así que puede entrar a "Nuevo producto"
además de comprar.

## Arquitectura

- **Una sola app** (`tienda`).
- **Vistas clásicas** (`views.py`, `urls.py`): login, registro, catálogo
  con filtros, crear producto. Sesión de Django, `layout.html` con
  Bootstrap.
- **Vistas DRF** (`api_views.py`, `api_urls.py`): detalle de producto y
  carrito. Autenticadas con la misma sesión (`SessionAuthentication`, sin
  JWT).
- La página `/productos/<id>/` no recibe los datos del producto por
  contexto de Django — los trae en vivo el JavaScript de `detalle.html`
  llamando a la API.

## Modelos

```
Categoria ──< Producto ──< ItemPedido >── Pedido >── User
```

`Pedido.estado` es `'carrito'` (en progreso) o `'confirmado'`. El carrito
de un usuario **es** su `Pedido` en estado `'carrito'` — no es una entidad
aparte.

