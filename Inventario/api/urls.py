from django.urls import path, include
from .views import *
urlpatterns = [
    path('v1/productos/', ProductoList.as_view(), name="producto_list"),
    path('v1/productos/<str:codigo>',
         ProductoDetalle.as_view(), name="producto_detalle"),
    path('v1/productos2/', productosList, name="producto_list2"),
    path('v1/productos2/<str:codigo>',
         productoDetalle, name="producto_detalle2"),
]
