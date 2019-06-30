from django.db import models
from bases.models import ClasesModelo


class Categoria(ClasesModelo):
    descripcion = models.CharField(
        max_length=100,
        help_text='Descripción de la Categoria',
        unique=True
    )

    def __str__(self):
        return '{}'.format(self.descripcion)

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

    class Meta:
        verbose_name_plural = "Unidades de Medida"


class Producto(ClasesModelo):
    codigo = models.CharField(
        max_length=20,
        unique=True
    )
    descripcion = models.CharField(max_length=200)
    existencia = models.IntegerField(default=0)
    stock_minimo = models.IntegerField()
    marca = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE)
    unidad_medida = models.ForeignKey(Marca, on_delete=models.CASCADE)
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.CASCADE)
