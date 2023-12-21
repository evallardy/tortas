from django.urls import path, include
from .views import *

urlpatterns = [
    path('', Elabora.as_view(), name='elabora'),
    path('nueva_torta/', nueva_torta, name='nueva_torta'),
    path('accion_torta/', accion_torta, name='accion_torta'),

    path('elabora', Elabora.as_view(), name='elabora'),
    path('pedir', Pedir.as_view(), name='pedir'),
    path('entrega', Entrega.as_view(), name='entrega'),

    path('ingredientes/', IngredienteListView.as_view(), name='ingrediente_list'),
    path('ingredientes/<int:pk>/', IngredienteDetailView.as_view(), name='ingrediente_detail'),
    path('ingredientes/nuevo/', IngredienteCreateView.as_view(), name='ingrediente_create'),
    path('ingredientes/editar/<int:pk>/', IngredienteUpdateView.as_view(), name='ingrediente_update'),
    path('ingredientes/eliminar/<int:pk>/', IngredienteDeleteView.as_view(), name='ingrediente_delete'),

    path('catalogo', Catalogo.as_view(), name='catalogo'),
    path('tortas/<int:pk>/', TortaDetailView.as_view(), name='torta_detail'),
    path('tortas/nuevo/', TortaCreateView.as_view(), name='torta_create'),
    path('tortas/editar/<int:pk>/', TortaUpdateView.as_view(), name='torta_update'),
    path('tortas/eliminar/<int:pk>/', TortaDeleteView.as_view(), name='torta_delete'),

    path('adicionales/', AdicionalListView.as_view(), name='adicional_list'),
    path('adicionales/nuevo/', AdicionalCreateView.as_view(), name='adicional_create'),
    path('adicionales/<int:pk>/', AdicionalUpdateView.as_view(), name='adicional_update'),
    path('adicionales/<int:pk>/eliminar/', AdicionalDeleteView.as_view(), name='adicional_delete'),
]