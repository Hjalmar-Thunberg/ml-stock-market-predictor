from django.db import models

class PredictionModel(models.Model):
    VERSIONS = []

    version = models.CharField(max_length=1000, choices=VERSIONS, null=True, blank=True)
    for_stock = models.CharField(max_length=10)
    num_nodes = 0
    acc_50 = 0
    acc_60 = 0
    acc_70 = 0
    acc_80 = 0
    acc_90 = 0
    acc_95 = 0
    acc_99 = 0

    def __str__(self):
        return "%s Prediction Model" % self.for_stock