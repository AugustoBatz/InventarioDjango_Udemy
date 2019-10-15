from django.db import models
from bases.models import ClasesModelo
from django.db.models.signals import post_save
from django.dispatch import receiver


class Categoria(ClasesModelo):
    descripcion = models.CharField(
        max_length=100,
        help_text='Descripción de la Categoria',
        unique=True
    )

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        id = Categoria.objects.all().count()
        if id:
            self.id = id+1
        else:
            self.id = 1
        self.descripcion = self.descripcion.upper()
        super(Categoria, self).save()

    class Meta:
        verbose_name_plural = "Categorias"


class SubCategoria(ClasesModelo):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descripcion = models.CharField(
        max_length=100,
        help_text='Descripción de la Categoria',

    )

    def __str__(self):
        return '{}:{}'.format(self.categoria.descripcion, self.descripcion)

    def save(self):
        id = SubCategoria.objects.all().count()
        if id:
            self.id = id+1
        else:
            self.id = 1
        self.descripcion = self.descripcion.upper()
        super(SubCategoria, self).save()

    class Meta:
        verbose_name_plural = "Sub-Categorias"
        unique_together = ('categoria', 'descripcion')


class Marca(ClasesModelo):
    descripcion = models.CharField(
        max_length=100,
        help_text='Descripcion de la Marca',
        unique=True
    )

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        id = Marca.objects.all().count()
        if id:
            self.id = id+1
        else:
            self.id = 1
        self.descripcion = self.descripcion.upper()
        super(Marca, self).save()

    class Meta:
        verbose_name_plural = "Marca"


class UnidadMedida(ClasesModelo):
    descripcion = models.CharField(
        max_length=100,
        help_text='Descripcion Unidad de Medida',
        unique=True
    )

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        id = UnidadMedida.objects.all().count()
        if id:
            self.id = id+1
        else:
            self.id = 1
        self.descripcion = self.descripcion.upper()
        super(UnidadMedida, self).save()

    class Meta:
        verbose_name_plural = "Unidades de Medida"


class Producto(ClasesModelo):

    codigo = models.CharField(
        max_length=20,
        unique=True,

    )
    descripcion = models.CharField(max_length=200)
    existencia = models.IntegerField(default=0)
    stock_minimo = models.IntegerField()
    precio_venta = models.FloatField()
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE)
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        if not self.id:
            productos = Producto.objects.filter(
                marca=self.marca, unidad_medida=self.unidad_medida, subcategoria=self.subcategoria).count()

            if productos:
                codigoCreate = str(1+productos)+"-"+str(self.marca.id)+"-" + \
                    str(self.unidad_medida.id)+"-"+str(self.subcategoria.id)
            else:
                codigoCreate = str(1)+"-"+str(self.marca.id)+"-" + \
                    str(self.unidad_medida.id)+"-"+str(self.subcategoria.id)
            self.codigo = codigoCreate
        self.descripcion = self.descripcion.upper()
        super(Producto, self).save()

    class Meta:
        verbose_name_plural = "Productos"
        unique_together = ('descripcion',
                           'unidad_medida', 'subcategoria', 'marca')
