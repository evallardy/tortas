from django.urls import path, include
from .views import *

urlpatterns = [
    path('', Elabora.as_view(), name='elabora'),
    path('nueva_torta/', nueva_torta, name='nueva_torta'),
    path('accion_torta/', accion_torta, name='accion_torta'),

    path('elabora', Elabora.as_view(), name='elabora'),
    path('pideNegocio', PideNegocio.as_view(), name='pide_negocio'),
#    path('pedir', Pedir.as_view(), name='pedir'),
    path('pideCliente', PideCliente.as_view(), name='pide_cliente'),
    path('ingredientes-torta/<int:pk>/', ingredientes_torta, name='ingredientes_torta'),
    path('verificaCliente', VerificaCliente.as_view(), name='verifica_cliente'),
    path('eliminaPedido/', eliminaPedido, name='elimina_pedido'),
    path('confirmadoPedido/', confirmadoPedido, name='confirmado_pedido'),
#    path('pideCliente/<uuid:token>/', PideCliente.as_view(), name='pide_cliente'),
    path('entrega', Entrega.as_view(), name='entrega'),
    path('pagaTorta', paga_torta, name='paga_torta'),

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

    path('precios/', PrecioTortasListView.as_view(), name='precio_list'),
    path('precios/nuevo/', PrecioTortasCreateView.as_view(), name='precio_create'),
    path('precios/<int:pk>/editar/', PrecioTortasUpdateView.as_view(), name='precio_update'),
    path('precios/<int:pk>/eliminar/', PrecioTortasDeleteView.as_view(), name='precio_delete'),

    path('reporte_pagos/', ReportePagosView.as_view(), name='reporte_pagos'),
    path('tortas-pago/<int:pk>/', tortas_pago, name='tortas_pago'),

    path('presenta_qr/', PresentaQRView.as_view(), name='presenta_qr'),
    path('solicitar/<uuid:token>/', SolicitarTortaView.as_view(), name='solicitar_musica'),
]