from django.db import models
from bases.models import ClasesModelo
from Inv.models import Producto
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum

# Create your models here.


class Cliente(ClasesModelo):
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
        max_length=20,
        null=True, blank=True
    )
    email = models.EmailField()
    nit = models.CharField(max_length=15, blank=False, null=False, unique=True)

    def __str__(self):
        return '{}, {}, {}'.format(self.nit, self.nombre, self.apellido)

    def save(self):
        self.nombre = self.nombre.upper()
        self.apellido = self.apellido.upper()
        self.direccion = self.direccion.upper()
        super(Cliente, self).save()

    class Meta:
        verbose_name_plural = "Clientes"


class Resoluciones(ClasesModelo):
    serie = models.CharField(
        max_length=45)
    rango_inicial = models.IntegerField()
    numero_resolucion = models.IntegerField()
    fecha_autorizacion = models.DateField()
    correlativo = models.IntegerField()
    rango_final = models.IntegerField()

    def __str__(self):
        return '{},{}'.format(self.serie, self.numero)

    class Meta:
        verbose_name_plural = "Resoluciones"
        verbose_name = "Resolucion"


class FacturaVenta(ClasesModelo):

    serie = models.CharField(
        max_length=45,
    )
    numero = models.IntegerField()
    total = models.FloatField(default=0)
    cantidad_producto = models.IntegerField(default=0)
    cliente = models.name = models.ForeignKey(
        Cliente, on_delete=models.CASCADE)
    fecha_compra = models.DateField()

    def __str__(self):
        return '{},{}'.format(self.serie, self.numero)

    def save(self):
        self.serie = self.serie.upper()

        super(FacturaVenta, self).save()

    class Meta:
        verbose_name_plural = "Encabezado Ventas"
        verbose_name = "Encabezado Venta"


class LoteVenta(ClasesModelo):
    noLote = models.IntegerField()
    fecha = models.DateField()
    cantidad = models.IntegerField()
    cantidad_inicial = models.IntegerField()
    costo_unitario = models.FloatField()
    costo_total = models.FloatField()
    # ganancia = models.FloatField()
    # precio_unitario = models.FloatField()
    # precio_total = models.FloatField()
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    facturaventa = models.ForeignKey(FacturaVenta, on_delete=models.CASCADE)

    def save(self):

        self.cantidad_inicial = self.cantidad
        # self.ganancia = 0
        # self.precio_unitario = 0
        # self.precio_total = 0
        self.costo_total = float(
            float(int(self.cantidad)) * float(self.costo_unitario))
        super(LoteVenta, self).save()
        # self.precio_total = float(
        #    float(int(self.cantidad)) * float(self.precio_unitario))
        # super(Lote, self).save()

    class Meta:
        verbose_name_plural = "Detalles Ventas"
        verbose_name = "Detalle Venta"


@receiver(post_save, sender=LoteVenta)
def detalle_compra_guardar(sender, instance, **kwargs):
    id_producto = instance.producto.id
    prod = Producto.objects.filter(pk=id_producto).first()

    if prod:
        cantidad = int(prod.existencia) - int(instance.cantidad)
        prod.existencia = cantidad
        prod.save()
