from django import forms
from .models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'imagen', 'categoria']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Figura Goku SSJ'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ej. Figura articulada de 18cm, edicion coleccionista'
            }),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripcion',
            'precio': 'Precio (S/)',
            'stock': 'Stock disponible',
        }

    # clean_nombre, clean_precio, clean_stock
    ### START CODE HERE ###
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre is None or not str(nombre).strip():
            raise forms.ValidationError("El nombre no puede quedar vacío.")
        return str(nombre).strip()

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is None or precio <= 0:
            raise forms.ValidationError("El precio no puede ser menor o igual a 0.")
        return precio

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is None or stock < 0:
            raise forms.ValidationError("El stock no puede ser negativo.")
        return stock
    ### END CODE HERE ###
