# Generated by Django 4.0 on 2021-12-25 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0012_alter_predictionmodel_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predictionmodel',
            name='version',
            field=models.IntegerField(default=1),
        ),
    ]