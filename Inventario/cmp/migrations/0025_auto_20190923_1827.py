# Generated by Django 2.2.2 on 2019-09-24 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmp', '0024_auto_20190923_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lote',
            name='costo_total',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='lote',
            name='costo_unitario',
            field=models.FloatField(default=0),
        ),
    ]