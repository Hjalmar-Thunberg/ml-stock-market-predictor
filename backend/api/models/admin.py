from django.contrib import admin

from models.models import PredictionModel
# Register your models here.
@admin.register(PredictionModel)
class PredictionModelAdmin(admin.ModelAdmin):
    list_display = (
        'for_stock',
        'version',
        'acc_50',
        'acc_60',
        'acc_70',
        'acc_80',
        'acc_90',
        'acc_95',
        'acc_99')
    fields = ['version']
        