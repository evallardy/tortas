from django.db import models
from django.contrib.auth.mixins import PermissionRequiredMixin

ESTATUS_TORTA = (
    (0, 'Pedida'),
    (1, 'Elaborada'),
    (2, 'Entregada'),
    (9, 'Cancelada'),
)
PARA = (
    (0, 'Comer'),
    (1, 'Llevar'),
)
PICANTE = (
    (0, 'Sin picante'),
    (1, 'Chipotle'),
    (2, 'Rajas'),
    (3, 'De los 2'),
)

class Ingrediente(models.Model, PermissionRequiredMixin):
    nombre = models.CharField("Ingrediente", max_length=100)
    precio = models.DecimalField("Precio", max_digits=6, decimal_places=2, default=0)
    activo = models.BooleanField('Activo', default=True)
    created = models.DateTimeField("Creado", auto_now_add=True)
    modified = models.DateTimeField("Actualizado", auto_now=True)

    class Meta:
        verbose_name = 'Ingrediente'
        verbose_name_plural = 'Ingredientes'
        ordering = ['nombre',]
        unique_together = ['nombre']
        db_table = 'Ingrediente'

    def __str__(self):   # para poner los nombres en los renglones
        return '%s' % (self.nombre)

class Torta(models.Model, PermissionRequiredMixin):
    nombre = models.CharField("Torta", max_length=200)
    ingredientes = models.ManyToManyField(Ingrediente, related_name='tortas')
    precio = models.DecimalField("Precio", max_digits=6, decimal_places=2, default=0)
    created = models.DateTimeField("Creado", auto_now_add=True)
    modified = models.DateTimeField("Actualizado", auto_now=True)

    class Meta:
        verbose_name = 'Torta'
        verbose_name_plural = 'Tortas'
        ordering = ['nombre',]
        unique_together = ['nombre']
        db_table = 'Torta'

    def __str__(self):   # para poner los nombres en los renglones
        return '%s' % (self.nombre)

class Pedido(models.Model, PermissionRequiredMixin):
    torta = models.CharField("Torta", max_length=100)
    donde = models.CharField("Donde", max_length=20)
    adicionales = models.CharField("Adicionales", max_length=100, null=True, blank=True)
    picante = models.JSONField("Picante", max_length=30)
    cantidad = models.IntegerField("Cantidad", default=0)
    precio = models.DecimalField("Precio", max_digits=6, decimal_places=2, default=0)
    activo = models.IntegerField('Activo', choices=ESTATUS_TORTA , default=0)
    created = models.DateTimeField("Creado", auto_now_add=True)
    modified = models.DateTimeField("Actualizado", auto_now=True)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['id',]
        db_table = 'Pedido'

    def __str__(self):   # para poner los nombres en los renglones
        return '%s %s %s %s %s' % (self.cantidad, self.torta, self.adicionales, self.picante, self.donde)

class Adicional(models.Model, PermissionRequiredMixin):
    nombre = models.CharField("Adicional", max_length=100)
    activo = models.BooleanField('Activo', default=True)
    created = models.DateTimeField("Creado", auto_now_add=True)
    modified = models.DateTimeField("Actualizado", auto_now=True)

    class Meta:
        verbose_name = 'Adicional'
        verbose_name_plural = 'Adicionales'
        ordering = ['nombre',]
        unique_together = ['nombre']
        db_table = 'Adicional'

    def __str__(self):   # para poner los nombres en los renglones
        return '%s' % (self.nombre)
