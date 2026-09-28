from django.contrib.auth.hashers import make_password
from django.db import migrations


def crear_datos_iniciales(apps, schema_editor):
    Categoria = apps.get_model('tienda', 'Categoria')
    Producto = apps.get_model('tienda', 'Producto')
    User = apps.get_model('auth', 'User')

    dragon_ball = Categoria.objects.create(nombre='Dragon Ball', descripcion='Figuras del universo de Dragon Ball')
    naruto = Categoria.objects.create(nombre='Naruto', descripcion='Figuras del universo ninja de Naruto')
    one_piece = Categoria.objects.create(nombre='One Piece', descripcion='Figuras de los piratas de One Piece')

    Producto.objects.create(nombre='Goku Super Saiyan', descripcion='Figura articulada de 18cm, edicion coleccionista', precio=129.90, stock=10, categoria=dragon_ball, imagen='productos/goku.png')
    Producto.objects.create(nombre='Vegeta SSJ Blue', descripcion='Figura de resina, 22cm, base incluida', precio=189.90, stock=5, categoria=dragon_ball, imagen='productos/vegeta.png')
    Producto.objects.create(nombre='Naruto Modo Sabio', descripcion='Figura articulada de 20cm con efectos de chakra', precio=149.90, stock=8, categoria=naruto, imagen='productos/naruto.png')
    Producto.objects.create(nombre='Sasuke Susanoo', descripcion='Figura de coleccion, 25cm', precio=219.90, stock=3, categoria=naruto, imagen='productos/sasuke.png')
    Producto.objects.create(nombre='Luffy Gear 5', descripcion='Figura articulada de 19cm, edicion limitada', precio=159.90, stock=6, categoria=one_piece, imagen='productos/luffy.png')
    Producto.objects.create(nombre='Zoro Three Sword Style', descripcion='Figura de resina, 21cm', precio=174.90, stock=0, categoria=one_piece, imagen='productos/zoro.png')

    if not User.objects.filter(username='demo').exists():
        User.objects.create(
            username='demo',
            email='demo@animefiguras.test',
            is_staff=True,
            password=make_password('DemoAnime#2024'),
        )


def eliminar_datos_iniciales(apps, schema_editor):
    Categoria = apps.get_model('tienda', 'Categoria')
    Categoria.objects.all().delete()

    User = apps.get_model('auth', 'User')
    User.objects.filter(username='demo').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(crear_datos_iniciales, eliminar_datos_iniciales),
    ]
