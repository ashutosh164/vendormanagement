from django.db import models


class Vendor(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=250)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=250, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0, blank=True, null=True)
    quality_rating_avg = models.FloatField(default=0.0, blank=True, null=True)
    average_response_time = models.FloatField(default=0.0, blank=True, null=True)
    fulfillment_rate = models.FloatField(default=0.0, blank=True, null=True)

    def __str__(self):
        return self.name

    def update_average_response_time(self):
        po_queryset = PurchaseOrder.objects.filter(vendor=self)
        acknowledged_po_queryset = po_queryset.filter(acknowledgment_date__isnull=False)
        if acknowledged_po_queryset.exists():
            total_response_time = sum(
                (acknowledged_po.acknowledgment_date - acknowledged_po.issue_date).total_seconds()
                for acknowledged_po in acknowledged_po_queryset
            )
            self.average_response_time = total_response_time / len(acknowledged_po_queryset)
        else:
            self.average_response_time = None
        self.save()

    def update_on_time_delivery_rate(self):
        completed_purchase_order = PurchaseOrder.objects.filter(vendor=self, status="Completed")
        if completed_purchase_order.count() > 0:
            on_time_purchase_orders = completed_purchase_order.filter(delivery_complete_date__gte=F('delivery_date'))
            on_time_delivery_data = on_time_purchase_orders.count() / completed_purchase_order.count()
            return on_time_delivery_data
        else:
            on_time_delivery_data = None
            return on_time_delivery_data

    def quality_rating_average(self):
        completed_purchase_orders_with_quality_rating = PurchaseOrder.objects.filter(vendor=self, status="Completed", quality_rating__isnull=False)
        quality_ratings = [item.quality_rating for item in completed_purchase_orders_with_quality_rating]
        if quality_ratings:
            calculate_quality_ratings_average = sum(quality_ratings) / len(quality_ratings)
            return calculate_quality_ratings_average
        else:
            calculate_quality_ratings_average = None
            return calculate_quality_ratings_average

    def calculate_average_response_time(self):
        completed_purchase_orders_with_acknowledgment = PurchaseOrder.objects.filter(vendor=self, acknowledgment_date__isnull=False)
        response_times = [(purchase_order.acknowledgment_date - purchase_order.issue_date).total_seconds() for purchase_order in completed_purchase_orders_with_acknowledgment]
        if response_times:
            average_response_time = sum(response_times) / len(response_times)
            return average_response_time
        else:
            average_response_time = None
            return average_response_time

    def fulfilment_rate(self):
        all_completed_status_without_issue = PurchaseOrder.objects.filter(vendor=self, status='Completed', issue_date__isnull=True)
        total_all = PurchaseOrder.objects.filter(vendor=self)
        if total_all.count() > 0:
            fulfilment_rate = all_completed_status_without_issue.count() / total_all.count()
            return fulfilment_rate
        else:
            fulfilment_rate = None
            return fulfilment_rate


class PurchaseOrder(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled')
    )
    objects = models.Manager()
    po_number = models.CharField(max_length=250, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now=True)
    delivery_date = models.DateTimeField(auto_now=True)
    items = models.JSONField(blank=True, null=True)
    quantity = models.IntegerField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)
    delivery_complete_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"PO #{self.po_number}"


class HistoricalPerformance(models.Model):
    objects = models.Manager()
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    on_time_delivery_rate = models.FloatField(blank=True, null=True)
    quality_rating_avg = models.FloatField(blank=True, null=True)
    average_response_time = models.FloatField(blank=True, null=True)
    fulfillment_rate = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"Historical Performance for {self.vendor} on {self.date}"




