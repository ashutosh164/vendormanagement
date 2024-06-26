from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import PurchaseOrder, HistoricalPerformance
from datetime import datetime


@receiver(post_save, sender=PurchaseOrder)
def set_delivery_complete_date(sender, created, instance, **kwargs):
    instance.vendor.update_average_response_time()
    instance.vendor.quality_rating_average()
    instance.vendor.calculate_average_response_time()
    instance.vendor.fulfilment_rate()
    if instance.status == 'Completed' and not instance.delivery_complete_date:
        instance.delivery_complete_date = timezone.now()
        instance.save()



