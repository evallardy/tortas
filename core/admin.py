from django.contrib import admin

from venta.models import *
from usuario.models import *

admin.site.register(Ingrediente)
admin.site.register(Torta)
admin.site.register(Pedido)
admin.site.register(Adicional)
admin.site.register(Usuario)

