from rest_framework import serializers

class PaymentCreateSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)
    currency = serializers.CharField(max_length=8)
    device_id = serializers.CharField(max_length=64)

class PaymentStatusSerializer(serializers.Serializer):
    status = serializers.CharField()

class WebhookSerializer(serializers.Serializer):
    payment_id = serializers.CharField(max_length=64)
    status = serializers.ChoiceField(choices=["paid", "failed"])