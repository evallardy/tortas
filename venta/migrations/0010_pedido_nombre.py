# Generated by Django 4.0.4 on 2025-05-06 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0009_pedido_solicitud_alter_pedido_donde_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='nombre',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Nombre'),
        ),
    ]
