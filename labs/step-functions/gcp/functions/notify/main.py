from datetime import datetime, timezone

import functions_framework


@functions_framework.http
def handler(request):
    order = request.get_json(silent=True) or {}
    email = order.get("customerEmail")
    print(f"[NOTIFY] Order {order.get('orderId')} confirmed — email to {email}")

    return (
        {
            "status": "COMPLETED",
            "orderId": order.get("orderId"),
            "paymentId": order.get("paymentId"),
            "notifiedAt": datetime.now(timezone.utc).isoformat(),
        },
        200,
    )
