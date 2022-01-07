from django.core.validators import MinValueValidator
from django.db import models

class PredictionModel(models.Model):
    VERSIONS = []

    version = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    for_stock = models.CharField(max_length=200)
    num_nodes = models.IntegerField(null=True)
    acc_50 = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    acc_60 = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    acc_70 = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    acc_80 = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    acc_90 = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    acc_95 = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    acc_99 = models.DecimalField(max_digits=4, decimal_places=2, null=True)

    def __str__(self):
        return "%s Prediction Model" % self.for_stock