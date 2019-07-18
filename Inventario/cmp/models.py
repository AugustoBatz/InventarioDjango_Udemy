from django.db import models
from bases.models import ClasesModelo
from Inv.models import Producto
# Create your models here.


class Proveedor(ClasesModelo):
    nombre = models.CharField(
        max_length=100,
        unique=True
    )
    apellido = models.CharField(
        max_length=100,
        unique=True
    )
    direccion = models.CharField(
        max_length=250,
        null=True, blank=True
    )
    telefono = models.CharField(
        max_length=10,
        null=True, blank=True
    )
    email = models.EmailField()
    nit = models.CharField(max_length=15, blank=False, null=False, unique=True)

    def __str__(self):
        return '{}, {}, {}'.format(self.nit, self.nombre, self.apellido)

    class Meta:
        verbose_name_plural = "Proveedores"


class FacturaCompra(ClasesModelo):
    serie = models.CharField(
        max_length=45,
    )
    numero = models.IntegerField()
    total = models.FloatField()
    cantidad_producto = models.IntegerField()
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha_compra = models.DateField()

    def __str__(self):
        return '{},{}'.format(self.serie, self.numero)

    class Meta:
        verbose_name_plural = "Encabezado Compras"
        verbose_name = "Encabezado Compra"


class Lote(ClasesModelo):
    noLote = models.IntegerField()
    fecha = models.DateField()
    cantidad = models.IntegerField()
    costo_unitario = models.FloatField()
    costo_total = models.FloatField()
    ganancia = models.FloatField()
    precio_unitario = models.FloatField()
    precio_total = models.FloatField()
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    facturacompra = models.ForeignKey(FacturaCompra, on_delete=models.CASCADE)

    def save(self):

        self.ganancia = 0
        self.precio_unitario = 0
        self.precio_total = 0
        self.costo_total = float(
            float(int(self.cantidad)) * float(self.costo_unitario))
        super(Lote, self).save()
        self.precio_total = float(
            float(int(self.cantidad)) * float(self.precio_unitario))
        super(Lote, self).save()

    class Meta:
        verbose_name_plural = "Detalles Compras"
        verbose_name = "Detalle Compra"
