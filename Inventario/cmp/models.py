from django.db import models
from bases.models import ClasesModelo
from Inv.models import Producto
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
# Create your models here.

# Para los signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from django.db.models.constraints import UniqueConstraint


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
    empresa = models.CharField(
        max_length=150,
        null=True, blank=True
    )
    direccion_empresa = models.CharField(
        max_length=150,
        null=True, blank=False
    )

    cuenta = models.IntegerField(null=True)

    telefono = models.CharField(
        max_length=10,
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
        self.empresa = self.empresa.upper()
        self.direccion_empresa = self.direccion_empresa.upper()
        self.nit = self.nit.upper()
        super(Proveedor, self).save()

    class Meta:
        verbose_name_plural = "Proveedores"


class FacturaCompra(ClasesModelo):
    serie = models.CharField(
        max_length=45,
    )
    numero = models.IntegerField()
    total = models.FloatField(default=0)
    cantidad_producto = models.IntegerField(default=0)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha_compra = models.DateField()

    def __str__(self):
        return '{},{}'.format(self.serie, self.numero)

    def save(self):
        self.serie = self.serie.upper()
        super(FacturaCompra, self).save()

    class Meta(object):

        verbose_name_plural = "Encabezado Compras"
        verbose_name = "Encabezado Compra"


class Lote(ClasesModelo):
    noLote = models.IntegerField()
    fecha = models.DateField()
    cantidad = models.IntegerField()
    cantidad_inicial = models.IntegerField()
    costo_unitario = models.FloatField(default=0)
    costo_total = models.FloatField(default=0)
    ganancia = models.FloatField()
    # precio_unitario = models.FloatField()
    # precio_total = models.FloatField()
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    facturacompra = models.ForeignKey(FacturaCompra, on_delete=models.CASCADE)

    def save(self):

        self.cantidad_inicial = self.cantidad
        # self.ganancia = 0
        # self.precio_unitario = 0
        # self.precio_total = 0
        self.costo_total = float(
            float(int(self.cantidad)) * float(self.costo_unitario))
        super(Lote, self).save()
        # self.precio_total = float(
        #    float(int(self.cantidad)) * float(self.precio_unitario))
        # super(Lote, self).save()

    class Meta:
        verbose_name_plural = "Detalles Compras"
        verbose_name = "Detalle Compra"


class Registro_Lote(ClasesModelo):
    noLote = models.IntegerField()
    fecha = models.DateField()
    cantidad = models.IntegerField()
    cantidad_inicial = models.IntegerField()
    costo_unitario = models.FloatField(default=0)
    costo_total = models.FloatField(default=0)
    ganancia = models.FloatField()
    # precio_unitario = models.FloatField()
    # precio_total = models.FloatField()
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    facturacompra = models.ForeignKey(FacturaCompra, on_delete=models.CASCADE)

    def save(self):

        self.cantidad_inicial = self.cantidad
        # self.ganancia = 0
        # self.precio_unitario = 0
        # self.precio_total = 0
        self.costo_total = float(
            float(int(self.cantidad)) * float(self.costo_unitario))
        super(Registro_Lote, self).save()
        # self.precio_total = float(
        #    float(int(self.cantidad)) * float(self.precio_unitario))
        # super(Lote, self).save()

    class Meta:
        verbose_name_plural = "Lotes Compras"
        verbose_name = "Lote Compra"


@receiver(post_delete, sender=Registro_Lote)
def detalle_compra_borrar(sender, instance, **kwargs):
    id_producto = instance.producto.id
    id_compra = instance.facturacompra.id
    Lote.objects.get(facturacompra=id_compra).delete()

    enc = FacturaCompra.objects.filter(pk=id_compra).first()
    if enc:
        total = Registro_Lote.objects.filter(
            facturacompra=id_compra).aggregate(Sum('costo_total'))

        cantidad = Registro_Lote.objects.filter(
            facturacompra=id_compra).aggregate(Sum('cantidad'))
        if total["costo_total__sum"] == None:
            total["costo_total__sum"] = 0
            cantidad["cantidad__sum"] = 0
            enc.delete()
        else:
            enc.cantidad_producto = cantidad["cantidad__sum"]
            enc.total = total["costo_total__sum"]

            enc.save()

    prod = Producto.objects.filter(pk=id_producto).first()
    if prod:
        cantidad = int(prod.existencia) - int(instance.cantidad)

        prod.existencia = cantidad
        prod.save()


@receiver(post_save, sender=Lote)
def detalle_compra_guardar(sender, instance, **kwargs):
    id_producto = instance.producto.id
    prod = Producto.objects.filter(pk=id_producto).first()
    cantidad = Lote.objects.filter(
        producto=prod, estado=True).aggregate(Sum('cantidad'))
    print("cantidad "+str(cantidad))
    print(cantidad["cantidad__sum"])
    if prod:
        if cantidad["cantidad__sum"]:
            prod.existencia = cantidad["cantidad__sum"]
        else:
            prod.existencia = 0
        prod.save()
