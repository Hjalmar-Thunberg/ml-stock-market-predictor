from django.contrib import admin
from models.views import _admin_model_train

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
    fields = ['for_stock', 'version', 'num_nodes']

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('for_stock',)
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if 'version' not in form.changed_data and 'num_nodes' in form.changed_data:
            stock = obj.for_stock
            num_nodes = int(form.cleaned_data['num_nodes'])
            _admin_model_train(stock, num_nodes)