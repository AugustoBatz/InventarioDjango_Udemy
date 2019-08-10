from django import forms
from .models import Cliente, FacturaVenta


class ClienteForm(forms.ModelForm):

    email = forms.EmailField(max_length=254)

    class Meta:
        model = Cliente
        exclude = ['um', 'fm', 'uc', 'fc']
        widget = {'nombre': forms.TextInput(), 'apellido': forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class FacturaVentaForm(forms.ModelForm):
    fecha_compra = forms.DateInput()

    class Meta:
        model = FacturaVenta
        fields = [
            'cliente',
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
