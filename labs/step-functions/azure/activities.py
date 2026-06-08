import uuid
from datetime import datetime, timezone

import azure.functions as func


def validate_order(order: dict) -> dict:
    order_id = order.get("orderId")
    email = order.get("customerEmail", "")
    amount = order.get("amount")

    if not order_id or not email or "@" not in email:
        raise ValueError("Invalid order: missing orderId or customerEmail")
    if amount is None or float(amount) <= 0:
        raise ValueError("Invalid order: amount must be > 0")

    return {**order, "validated": True, "currency": order.get("currency", "BRL")}


def process_payment(order: dict) -> dict:
    if order.get("simulateFailure"):
        raise RuntimeError("Payment declined (simulated)")

    amount = float(order.get("amount", 0))
    if amount > 10000:
        raise RuntimeError("Payment declined: amount exceeds limit")

    return {
        **order,
        "paymentId": f"pay-{uuid.uuid4().hex[:12]}",
        "paid": True,
    }


def send_notification(order: dict) -> dict:
    email = order.get("customerEmail")
    print(f"[NOTIFY] Order {order.get('orderId')} confirmed — email to {email}")

    return {
        "status": "COMPLETED",
        "orderId": order.get("orderId"),
        "paymentId": order.get("paymentId"),
        "notifiedAt": datetime.now(timezone.utc).isoformat(),
    }
