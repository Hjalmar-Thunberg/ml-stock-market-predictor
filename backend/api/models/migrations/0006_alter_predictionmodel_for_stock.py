# Generated by Django 4.0 on 2021-12-25 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0005_alter_predictionmodel_path_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predictionmodel',
            name='for_stock',
            field=models.CharField(max_length=200),
        ),
    ]
