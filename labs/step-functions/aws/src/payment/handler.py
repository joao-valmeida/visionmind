import uuid


def lambda_handler(event, context):
    if event.get("simulateFailure"):
        raise RuntimeError("Payment declined (simulated)")

    amount = float(event.get("amount", 0))
    if amount > 10000:
        raise RuntimeError("Payment declined: amount exceeds limit")

    return {
        **event,
        "paymentId": f"pay-{uuid.uuid4().hex[:12]}",
        "paid": True,
    }
