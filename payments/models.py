from django.db import models

class Payment(models.Model):
    STATUS_PENDING = "pending"
    STATUS_PAID = "paid"
    STATUS_FAILED = "failed"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_PAID, "Paid"),
        (STATUS_FAILED, "Failed"),
    ]

    amount = models.PositiveIntegerField()
    currency = models.CharField(max_length=8, default="KGS")
    device_id = models.CharField(max_length=64)

    payment_id = models.CharField(max_length=64, unique=True)  # id от платёжки/провайдера
    qr_data = models.TextField()  # ссылка/строка для QR

    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_PENDING)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.payment_id} ({self.status})"

class Device(models.Model):
    name = models.CharField(max_length=64)
    device_id = models.CharField(max_length=64, unique=True)
    api_key = models.CharField(max_length=64, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.device_id