# Generated by Django 2.0.1 on 2018-04-12 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0002_auto_20180331_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='validacion',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='patient',
            name='diabetes',
            field=models.NullBooleanField(default=None),
        ),
        migrations.AlterField(
            model_name='patient',
            name='hab_calle',
            field=models.NullBooleanField(default=None),
        ),
        migrations.AlterField(
            model_name='patient',
            name='info_clinica',
            field=models.NullBooleanField(default=None),
        ),
        migrations.AlterField(
            model_name='patient',
            name='sexo',
            field=models.NullBooleanField(default=None),
        ),
        migrations.AlterField(
            model_name='patient',
            name='vih',
            field=models.NullBooleanField(default=None),
        ),
    ]
