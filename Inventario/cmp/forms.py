from django import forms
from .models import Proveedor, FacturaCompra


class ProveedorForm(forms.ModelForm):

    email = forms.EmailField(max_length=254)

    class Meta:
        model = Proveedor
        exclude = ['um', 'fm', 'uc', 'fc']
        widget = {'nombre': forms.TextInput(), 'apellido': forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class FacturaCompraForm(forms.ModelForm):
    fecha_compra = forms.DateInput()

    class Meta:
        model = FacturaCompra
        fields = [
            'proveedor',
            'fecha_compra',
            'serie',
            'numero',
            'cantidad_producto',
            'total'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['cantidad_producto'].widget.attrs['readonly'] = True
        self.fields['total'].widget.attrs['readonly'] = True
        self.fields['fecha_compra'].widget.attrs['readonly'] = True
