# Generated by Django 4.0.4 on 2025-05-08 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0015_pagos_importe_real'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preciotortasingredientes',
            name='pago',
        ),
        migrations.AddField(
            model_name='pedido',
            name='pago',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='venta.pagos'),
        ),
    ]
