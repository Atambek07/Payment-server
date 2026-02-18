from django.urls import path
from .views import PaymentCreateView, PaymentStatusView, PaymentWebhookView

urlpatterns = [
    path("create", PaymentCreateView.as_view()),
    path("status", PaymentStatusView.as_view()),
    path("webhook", PaymentWebhookView.as_view()),
]