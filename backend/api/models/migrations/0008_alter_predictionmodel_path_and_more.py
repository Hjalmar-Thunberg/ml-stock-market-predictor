# Generated by Django 4.0 on 2021-12-25 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0007_predictionmodel_num_nodes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predictionmodel',
            name='path',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='predictionmodel',
            name='version',
            field=models.CharField(choices=[], default='', max_length=1),
        ),
    ]