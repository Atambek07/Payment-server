import uuid

class MockPaymentProvider:
    """
    Заглушка платёжной системы:
    - create_payment возвращает payment_id и qr_data
    - validate_webhook всегда True (потом будет подпись/секрет)
    """

    def create_payment(self, amount: int, currency: str, device_id: str) -> dict:
        pid = uuid.uuid4().hex[:12]
        qr_data = f"https://pay.mock/{pid}"
        return {"payment_id": pid, "qr_data": qr_data}

    def validate_webhook(self, request) -> bool:
        return True