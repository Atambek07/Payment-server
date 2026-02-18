from django.urls import path
from .views import PaymentCreateView, PaymentStatusView, PaymentWebhookView, PaymentQRView

urlpatterns = [
    path("create", PaymentCreateView.as_view()),
    path("status", PaymentStatusView.as_view()),
    path("webhook", PaymentWebhookView.as_view()),
    path("qr", PaymentQRView.as_view()),
]