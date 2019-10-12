from django.urls import path
from .views import *

urlpatterns = [
    path('clientes/', ClienteView.as_view(), name="cliente_list"),
    path('clientes/new', ClienteNew.as_view(), name="cliente_new"),
    path('clientes/<int:pk>', ClienteEdit.as_view(), name="cliente_edit"),
    path('clientes/estado/<int:id>', clienteInactivar, name="cliente_inactivar"),

    path('ventas/', FacturaVentaView.as_view(), name="ventas_list"),
    path('ventas/reporte', reporte_ventas, name="ventas_reporte"),

    path('ventas/new', ventas2, name="ventas_new"),
    path('ventas/edit/<int:facturaventa_id>', ventas2, name="ventas_edit"),

    #
    path('ventas2/new', ventas, name="ventas_new2"),
    path('ventas2/edit/<int:facturaventa_id>', ventas, name="ventas_edit2"),
    path('ventas/buscarProducto', ProductoView.as_view(), name="compra_producto"),
    path('ventas/print', reporte_ventasPDF, name="fac_print")
    # path('ventas/<int:facturventa_id>/delete/<int:pk>',
    #     CompraDetDelete.as_view(), name="ventas_del"),
    #path('ventas/listado', reporte_compras, name="ventas_print_all")
]
