# Generated by Django 2.2.2 on 2019-09-05 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmp', '0019_auto_20190904_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facturacompra',
            name='numero',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='facturacompra',
            name='serie',
            field=models.CharField(max_length=45),
        ),
    ]