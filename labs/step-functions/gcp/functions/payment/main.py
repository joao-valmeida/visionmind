import uuid

import functions_framework


@functions_framework.http
def handler(request):
    order = request.get_json(silent=True) or {}

    if order.get("simulateFailure"):
        return ({"error": "Payment declined (simulated)"}, 402)

    amount = float(order.get("amount", 0))
    if amount > 10000:
        return ({"error": "Payment declined: amount exceeds limit"}, 402)

    return (
        {
            **order,
            "paymentId": f"pay-{uuid.uuid4().hex[:12]}",
            "paid": True,
        },
        200,
    )
