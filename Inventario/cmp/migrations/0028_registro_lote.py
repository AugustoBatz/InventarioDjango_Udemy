# Generated by Django 2.2.2 on 2019-09-27 01:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Inv', '0009_auto_20190923_1741'),
        ('fac', '0004_auto_20190907_2048'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cmp', '0027_auto_20190923_1947'),
    ]

    operations = [
        migrations.CreateModel(
            name='Registro_Lote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('fc', models.DateTimeField(auto_now_add=True)),
                ('fm', models.DateTimeField(auto_now=True)),
                ('um', models.IntegerField(blank=True, null=True)),
                ('noLote', models.IntegerField()),
                ('fecha', models.DateField()),
                ('cantidad', models.IntegerField()),
                ('cantidad_inicial', models.IntegerField()),
                ('costo_unitario', models.FloatField(default=0)),
                ('costo_total', models.FloatField(default=0)),
                ('facturacompra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmp.FacturaCompra')),
                ('loteventa', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fac.LoteVenta')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Inv.Producto')),
                ('uc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Lote Compra',
                'verbose_name_plural': 'Lotes Compras',
            },
        ),
    ]
