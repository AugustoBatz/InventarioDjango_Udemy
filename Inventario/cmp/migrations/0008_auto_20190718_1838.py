# Generated by Django 2.2.2 on 2019-07-19 00:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmp', '0007_auto_20190701_1533'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lote',
            name='ganancia',
        ),
        migrations.RemoveField(
            model_name='lote',
            name='precio_total',
        ),
        migrations.RemoveField(
            model_name='lote',
            name='precio_unitario',
        ),
    ]