# Generated by Django 4.2.7 on 2023-11-21 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacionAdministrador', '0006_emergencias'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emergencias',
            name='emergencias_unidades',
        ),
        migrations.RemoveField(
            model_name='emergencias',
            name='emergencias_voluntarios',
        ),
        migrations.AddField(
            model_name='emergencias',
            name='unidades_in_emer',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='emergencias',
            name='voluntarios_in_emer',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='unidades',
            name='emergencia_atendida',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='voluntarios',
            name='unidad_asignada',
            field=models.CharField(default='', max_length=5),
        ),
    ]
