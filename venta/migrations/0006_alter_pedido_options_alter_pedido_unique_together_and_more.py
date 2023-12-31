# Generated by Django 4.0.4 on 2023-12-16 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0005_rename_adicionales_adicional'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pedido',
            options={'ordering': ['id'], 'verbose_name': 'Pedido', 'verbose_name_plural': 'Pedidos'},
        ),
        migrations.AlterUniqueTogether(
            name='pedido',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='pedido',
            name='cantidad',
            field=models.IntegerField(default=0, verbose_name='Cantidad'),
        ),
        migrations.AddField(
            model_name='pedido',
            name='donde',
            field=models.CharField(default='1', max_length=20, verbose_name='Donde'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pedido',
            name='picante',
            field=models.JSONField(default='1', max_length=30, verbose_name='Picante'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pedido',
            name='torta',
            field=models.CharField(default='1', max_length=100, verbose_name='Torta'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pedido',
            name='adicionales',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Adicionales'),
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='nombre',
        ),
    ]
