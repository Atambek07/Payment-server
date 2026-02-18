from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as http_status
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from io import BytesIO

from .models import Payment
from .serializers import PaymentCreateSerializer, WebhookSerializer
from .provider import MockPaymentProvider

provider = MockPaymentProvider()

class PaymentCreateView(APIView):
    def post(self, request):
        ser = PaymentCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        amount = ser.validated_data["amount"]
        currency = ser.validated_data["currency"]
        device_id = ser.validated_data["device_id"]

        # 1) создать у провайдера
        created = provider.create_payment(amount, currency, device_id)

        # 2) сохранить в БД
        p = Payment.objects.create(
            amount=amount,
            currency=currency,
            device_id=device_id,
            payment_id=created["payment_id"],
            qr_data=created["qr_data"],
            status=Payment.STATUS_PENDING,
        )

        return Response(
            {"payment_id": p.payment_id, "qr_data": p.qr_data},
            status=http_status.HTTP_201_CREATED,
        )


class PaymentStatusView(APIView):
    def get(self, request):
        pid = request.query_params.get("id")
        if not pid:
            return Response({"detail": "Missing id"}, status=http_status.HTTP_400_BAD_REQUEST)

        p = get_object_or_404(Payment, payment_id=pid)
        return Response({"status": p.status})


class PaymentWebhookView(APIView):
    authentication_classes = []  # пока без auth
    permission_classes = []

    def post(self, request):
        # 1) валидация подписи (пока заглушка)
        if not provider.validate_webhook(request):
            return Response({"detail": "Invalid signature"}, status=http_status.HTTP_401_UNAUTHORIZED)

        # 2) валидируем тело
        ser = WebhookSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        pid = ser.validated_data["payment_id"]
        new_status = ser.validated_data["status"]

        p = get_object_or_404(Payment, payment_id=pid)

        if new_status == "paid":
            p.status = Payment.STATUS_PAID
        else:
            p.status = Payment.STATUS_FAILED

        p.save(update_fields=["status", "updated_at"])
        return Response({"ok": True})
