from datetime import datetime, timezone


def lambda_handler(event, context):
    email = event.get("customerEmail")
    print(f"[NOTIFY] Order {event.get('orderId')} confirmed — email to {email}")

    return {
        "status": "COMPLETED",
        "orderId": event.get("orderId"),
        "paymentId": event.get("paymentId"),
        "notifiedAt": datetime.now(timezone.utc).isoformat(),
    }
