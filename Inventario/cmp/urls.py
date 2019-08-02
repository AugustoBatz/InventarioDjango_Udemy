from django.urls import path

from .views import *
from .reportes import reporte_compras
urlpatterns = [
    path('proveedores/', ProveedorView.as_view(), name="proveedor_list"),
    path('proveedores/new', ProveedorNew.as_view(), name="proveedor_new"),
    path('proveedores/edit/<int:pk>',
         ProveedorEdit.as_view(), name="proveedor_edit"),
    path('proveedor/inactivar/<int:id>',
         proveedorInactivar, name="proveedor_ina"),

    path('compras/', FacturaCompraView.as_view(), name="compras_list"),
    path('compras/new', compras, name="compras_new"),
    path('compras/edit/<int:facturacompra_id>', compras, name="compras_edit"),

    path('compras/<int:facturacompra_id>/delete/<int:pk>',
         CompraDetDelete.as_view(), name="compras_del"),
    path('compras/listado', reporte_compras, name="compras_print_all")

]
