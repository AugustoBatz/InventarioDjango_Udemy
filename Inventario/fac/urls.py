from django.urls import path
from .views import *

urlpatterns = [
    path('clientes/', ClienteView.as_view(), name="cliente_list"),
    path('clientes/new', ClienteNew.as_view(), name="cliente_new"),
    path('clientes/<int:pk>', ClienteEdit.as_view(), name="cliente_edit"),
    path('clientes/estado/<int:id>', clienteInactivar, name="cliente_inactivar"),

    path('ventas/', FacturaVentaView.as_view(), name="ventas_list"),
    path('ventas/new', ventas, name="ventas_new"),
    path('ventas/edit/<int:facturaventa_id>', ventas, name="ventas_edit"),
    # path('ventas/<int:facturventa_id>/delete/<int:pk>',
    #     CompraDetDelete.as_view(), name="ventas_del"),
    #path('ventas/listado', reporte_compras, name="ventas_print_all")
]
