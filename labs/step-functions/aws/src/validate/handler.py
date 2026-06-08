def lambda_handler(event, context):
    order_id = event.get("orderId")
    email = event.get("customerEmail", "")
    amount = event.get("amount")

    if not order_id or not email or "@" not in email:
        raise ValueError("Invalid order: missing orderId or customerEmail")
    if amount is None or float(amount) <= 0:
        raise ValueError("Invalid order: amount must be > 0")

    return {**event, "validated": True, "currency": event.get("currency", "BRL")}
