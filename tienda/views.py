from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib import messages

from .models import Categoria, Producto
from .forms import ProductoForm


def ingreso(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('tienda:catalogo'))
        messages.error(request, "Usuario o contraseña incorrectos")
        return HttpResponseRedirect(reverse('tienda:ingreso'))
    return render(request, 'ingreso.html')


def registro(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, "El usuario y la contraseña son obligatorios")
            return HttpResponseRedirect(reverse('tienda:registro'))

        if User.objects.filter(username=username).exists():
            messages.error(request, "Este nombre de usuario ya existe")
            return HttpResponseRedirect(reverse('tienda:registro'))

        if email and User.objects.filter(email__iexact=email).exists():
            messages.error(request, "Ese email ya esta registrado")
            return HttpResponseRedirect(reverse('tienda:registro'))

        try:
            validate_password(password)
        except DjangoValidationError as e:
            for msg in e.messages:
                messages.error(request, msg)
            return HttpResponseRedirect(reverse('tienda:registro'))

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Cuenta creada. Ya puedes ingresar")
        return HttpResponseRedirect(reverse('tienda:ingreso'))
    return render(request, 'registro.html')


@login_required
def cerrar_sesion(request):
    logout(request)
    return HttpResponseRedirect(reverse('tienda:ingreso'))


@login_required
def catalogo(request):
    productos = Producto.objects.select_related('categoria').all()

    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    query = request.GET.get('q')
    if query:
        productos = productos.filter(nombre__icontains=query)

    return render(request, 'catalogo.html', {
        'productos': productos,
        'categorias': Categoria.objects.all(),
        'categoria_seleccionada': int(categoria_id) if categoria_id else None,
        'query': query or '',
    })


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='tienda:catalogo')
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente")
            return HttpResponseRedirect(reverse('tienda:catalogo'))
    else:
        form = ProductoForm()
    return render(request, 'crear_producto.html', {'form': form})


@login_required
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'detalle.html', {'producto_id': producto.id})
