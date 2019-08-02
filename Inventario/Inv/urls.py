from django.urls import path
from .views import *

urlpatterns = [
    path('categorias/', CategoriaView.as_view(), name='categoria_list'),
    path('categoria/new', CategoriaNew.as_view(), name='categoria_new'),
    path('categoria/edit/<int:pk>', CategoriaEdit.as_view(), name='categoria_edit'),

    # sub cateogiras

    path('subcategorias/', SubCategoriaView.as_view(), name='subcategoria_list'),
    path('subcategorias/new', SubCategoriaNew.as_view(), name='subcategoria_new'),
    path('subcategorias/edit/<int:pk>',
         SubCategoriaEdit.as_view(), name='subcategoria_edit'),
    # Marca
    path('marcas/', MarcaView.as_view(), name='marca_list'),
    path('marcas/new', MarcaNew.as_view(), name='marca_new'),
    path('marcas/edit/<int:pk>', MarcaEdit.as_view(), name='marca_edit'),
    ### ruta para vistas basadas en funciones #####
    path('marcas/inactivar/<int:id>', marca_inactivar, name="marca_inactivar"),
    ########## Unidad de medida ######
    path('um/', UMView.as_view(), name='um_list'),
    path('um/new', UMNew.as_view(), name='um_new'),
    path('um/edit/<int:pk>', UMEdit.as_view(), name='um_edit'),
    # Productos
    path('producto/', ProductoView.as_view(), name='producto_list'),
    path('producto/new', ProductoNew.as_view(), name='producto_new'),
    path('producto/edit/<int:pk>', ProductoEdit.as_view(), name='producto_edit'),
    path('producto/lotes/<int:idProd>', verLotes, name='lote_list'),
]
