# Generated by Django 2.2 on 2019-06-01 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage_go_app', '0002_activeuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='statistic',
            name='value',
            field=models.CharField(default='', max_length=100, verbose_name='Valor'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='statistic',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Nombre'),
        ),
    ]
