# Generated by Django 4.0 on 2021-12-25 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0010_remove_predictionmodel_acc_50_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='predictionmodel',
            name='acc_50',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='predictionmodel',
            name='acc_60',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='predictionmodel',
            name='acc_70',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='predictionmodel',
            name='acc_80',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='predictionmodel',
            name='acc_90',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='predictionmodel',
            name='acc_95',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='predictionmodel',
            name='acc_99',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='predictionmodel',
            name='num_nodes',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='predictionmodel',
            name='for_stock',
            field=models.CharField(max_length=200),
        ),
    ]
