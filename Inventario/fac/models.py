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

    class Meta:
        verbose_name_plural = "Clientes"


class FacturaVenta(ClasesModelo):
    serie = models.CharField(
        max_length=45,
    )
    numero = models.IntegerField()
    total = models.FloatField()
    cantidad_producto = models.IntegerField()
    cliente = models.name = models.ForeignKey(
        Cliente, on_delete=models.CASCADE)
    fecha_compra = models.DateField()

    def __str__(self):
        return '{},{}'.format(self.serie, self.numero)

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
    #ganancia = models.FloatField()
    #precio_unitario = models.FloatField()
    #precio_total = models.FloatField()
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    facturaventa = models.ForeignKey(FacturaVenta, on_delete=models.CASCADE)

    def save(self):

        self.cantidad_inicial = self.cantidad
        #self.ganancia = 0
        #self.precio_unitario = 0
        #self.precio_total = 0
        self.costo_total = float(
            float(int(self.cantidad)) * float(self.costo_unitario))
        super(LoteVenta, self).save()
        # self.precio_total = float(
        #    float(int(self.cantidad)) * float(self.precio_unitario))
        #super(Lote, self).save()

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
