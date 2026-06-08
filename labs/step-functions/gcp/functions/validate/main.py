import functions_framework


@functions_framework.http
def handler(request):
    order = request.get_json(silent=True) or {}
    order_id = order.get("orderId")
    email = order.get("customerEmail", "")
    amount = order.get("amount")

    if not order_id or not email or "@" not in email:
        return ({"error": "Invalid order: missing orderId or customerEmail"}, 400)
    if amount is None or float(amount) <= 0:
        return ({"error": "Invalid order: amount must be > 0"}, 400)

    return ({**order, "validated": True, "currency": order.get("currency", "BRL")}, 200)
