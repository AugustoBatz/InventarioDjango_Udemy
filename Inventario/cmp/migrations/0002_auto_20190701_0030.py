# Generated by Django 2.2.2 on 2019-07-01 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proveedor',
            name='nit',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]