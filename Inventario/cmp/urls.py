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

    path('compras/new', compras2, name="compras_new"),
    path('compras/edit/<int:facturacompra_id>', compras2, name="compras_edit"),
    path('compras/anular/<int:id>', anularCompra, name="desactivarFactura"),
    ##
    path('compras/canceladas', FacturaCompraCanView.as_view(),
         name="compras_canceladas"),
    path('compras/compra-cancelada/<int:facturacompra_id>',
         compra_cancelada, name="compras_cancelada"),
    #
    path('compras2/new', compras, name="compras_new2"),
    path('compras2/edit/<int:facturacompra_id>',
         compras, name="compras_edit2"),
    #
    path('compras/<int:facturacompra_id>/delete/<int:pk>',
         CompraDetDelete.as_view(), name="compras_del"),
    path('compras/listado', reporte_compras, name="compras_print_all"),
    path('compras/buscarProducto', ProductoView.as_view(), name="compra_producto"),

]
