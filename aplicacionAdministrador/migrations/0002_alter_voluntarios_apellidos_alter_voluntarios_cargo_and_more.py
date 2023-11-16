# Generated by Django 4.2.4 on 2023-11-12 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacionAdministrador', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voluntarios',
            name='apellidos',
            field=models.CharField(default='', max_length=40),
        ),
        migrations.AlterField(
            model_name='voluntarios',
            name='cargo',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='voluntarios',
            name='compania',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='voluntarios',
            name='direccion',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='voluntarios',
            name='nombres',
            field=models.CharField(default='', max_length=40),
        ),
        migrations.AlterField(
            model_name='voluntarios',
            name='numero_registro',
            field=models.IntegerField(default=0, unique=True),
        ),
        migrations.AlterField(
            model_name='voluntarios',
            name='telefono',
            field=models.PositiveBigIntegerField(blank=True, default=0),
        ),
    ]
