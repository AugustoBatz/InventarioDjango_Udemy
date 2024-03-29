# Generated by Django 2.2.2 on 2019-07-01 20:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Inv', '0006_auto_20190630_2356'),
        ('cmp', '0002_auto_20190701_0030'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacturaCompra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('fc', models.DateTimeField(auto_now_add=True)),
                ('fm', models.DateTimeField(auto_now=True)),
                ('um', models.IntegerField(blank=True, null=True)),
                ('serie', models.CharField(max_length=45)),
                ('numero', models.IntegerField()),
                ('total', models.FloatField()),
                ('fecha', models.DateField()),
                ('cantidad_producto', models.IntegerField()),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmp.Proveedor')),
                ('uc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Encabezado Compra',
                'verbose_name_plural': 'Encabezado Compras',
            },
        ),
        migrations.CreateModel(
            name='Lote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('fc', models.DateTimeField(auto_now_add=True)),
                ('fm', models.DateTimeField(auto_now=True)),
                ('um', models.IntegerField(blank=True, null=True)),
                ('noLote', models.IntegerField()),
                ('fecha', models.DateField()),
                ('cantidad', models.IntegerField()),
                ('costo_unitario', models.FloatField()),
                ('costo_total', models.FloatField()),
                ('ganancia', models.FloatField()),
                ('precio_unitario', models.FloatField()),
                ('precio_total', models.FloatField()),
                ('facturacompra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmp.FacturaCompra')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Inv.Producto')),
                ('uc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
