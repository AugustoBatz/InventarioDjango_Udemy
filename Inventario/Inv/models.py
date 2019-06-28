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
