from rest_framework import serializers, status
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .models import Vendor, PurchaseOrder
User = get_user_model()
from django.db.models import Q, F


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('email')
        password = data.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if not user:
                message = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(message, code='authorization')
        else:
            message = 'Must include "username" and "password".'
            raise serializers.ValidationError(message, code='authorization')
        data['user'] = user
        return data


class VendorSerializer(serializers.ModelSerializer):
    # on_time_delivery_rate = serializers.SerializerMethodField()
    # quality_rating_average = serializers.SerializerMethodField()
    calculate_average_response_time = serializers.SerializerMethodField()
    # fulfilment_rate = serializers.SerializerMethodField()

    def get_calculate_average_response_time(self, obj):
        completed_purchase_orders_with_acknowledgment = PurchaseOrder.objects.filter(vendor=obj, acknowledgment_date__isnull=False)
        response_times = [(purchase_order.acknowledgment_date - purchase_order.issue_date).total_seconds() for purchase_order in completed_purchase_orders_with_acknowledgment]
        if response_times:
            average_response_time = sum(response_times) / len(response_times)
            return average_response_time
        else:
            average_response_time = None
            return average_response_time

    class Meta:
        model = Vendor
        fields = '__all__'


class VendorPerformanceSerializer(serializers.ModelSerializer):
    on_time_delivery_rate = serializers.SerializerMethodField()
    quality_rating_average = serializers.SerializerMethodField()
    calculate_average_response_time = serializers.SerializerMethodField()
    fulfilment_rate = serializers.SerializerMethodField()

    class Meta:
        model = Vendor
        fields = '__all__'

    def get_on_time_delivery_rate(self, obj):
        # completed_purchase_orders = PurchaseOrder.objects.filter(vendor=obj, status='Completed')
        # if completed_purchase_orders.count() > 0:
        #     on_time_purchase_orders = completed_purchase_orders.filter(delivery_date__gte=F('order_date'))
        #     on_time_delivery_rate = on_time_purchase_orders.count() / completed_purchase_orders.count()
        #     return on_time_delivery_rate
        completed_purchase_order = PurchaseOrder.objects.filter(vendor=obj, status="Completed")
        if completed_purchase_order.count() > 0:
            on_time_purchase_orders = completed_purchase_order.filter(delivery_complete_date__gte=F('delivery_date'))
            on_time_delivery_data = on_time_purchase_orders.count() / completed_purchase_order.count()
            return on_time_delivery_data
        else:
            on_time_delivery_data = None
            return on_time_delivery_data

    def get_quality_rating_average(self, obj):
        completed_purchase_orders_with_quality_rating = PurchaseOrder.objects.filter(vendor=obj, status="Completed", quality_rating__isnull=False)
        quality_ratings = [item.quality_rating for item in completed_purchase_orders_with_quality_rating]
        if quality_ratings:
            calculate_quality_ratings_average = sum(quality_ratings) / len(quality_ratings)
            return calculate_quality_ratings_average
        else:
            calculate_quality_ratings_average = None
            return calculate_quality_ratings_average

    def get_calculate_average_response_time(self, obj):
        completed_purchase_orders_with_acknowledgment = PurchaseOrder.objects.filter(vendor=obj, acknowledgment_date__isnull=False)
        response_times = [(purchase_order.acknowledgment_date - purchase_order.issue_date).total_seconds() for purchase_order in completed_purchase_orders_with_acknowledgment]
        if response_times:
            average_response_time = sum(response_times) / len(response_times)
            return average_response_time
        else:
            average_response_time = None
            return average_response_time

    def get_fulfilment_rate(self, obj):
        all_completed_status_without_issue = PurchaseOrder.objects.filter(vendor=obj, status='Completed', issue_date__isnull=True)
        total_all = PurchaseOrder.objects.filter(vendor=obj)
        if total_all.count() > 0:
            fulfilment_rate = all_completed_status_without_issue.count() / total_all.count()
            return fulfilment_rate
        else:
            fulfilment_rate = None
            return fulfilment_rate


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'


class PurchaseOrderAcknowledgmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['acknowledgment_date']

