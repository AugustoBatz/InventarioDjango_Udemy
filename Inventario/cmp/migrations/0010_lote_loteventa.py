# Generated by Django 2.2.2 on 2019-08-08 03:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fac', '0002_facturaventa_loteventa'),
        ('cmp', '0009_lote_cantidad_inicial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lote',
            name='loteventa',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='fac.LoteVenta'),
            preserve_default=False,
        ),
    ]
