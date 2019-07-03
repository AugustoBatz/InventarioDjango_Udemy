from django.urls import path
from .views import *

urlpatterns = [
    path('proveedores/', ProveedorView.as_view(), name="proveedor_list"),
    path('proveedores/new', ProveedorNew.as_view(), name="proveedor_new"),
    path('proveedores/edit/<int:pk>',
         ProveedorEdit.as_view(), name="proveedor_edit"),
    path('proveedor/inactivar/<int:id>',
         proveedorInactivar, name="proveedor_ina"),

    path('compras/', FacturaCompraView.as_view(), name="compras_list"),
    path('compras/new', compras, name="compras_new"),
]
