import json

import azure.durable_functions as df
import azure.functions as func

from activities import process_payment, send_notification, validate_order

app = df.DFApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.route(route="orders", methods=["POST"])
@app.durable_client_input(client_name="client")
async def order_http(req: func.HttpRequest, client):
    try:
        order = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    instance_id = await client.start_new("order_orchestrator", None, order)
    return client.create_check_status_response(req, instance_id)


@app.orchestration_trigger(context_name="context")
def order_orchestrator(context: df.DurableOrchestrationContext):
    order = context.get_input()

    try:
        validated = yield context.call_activity("validate_order_activity", order)
        paid = yield context.call_activity("process_payment_activity", validated)
        result = yield context.call_activity("send_notification_activity", paid)
        return result
    except Exception as exc:
        return {
            "status": "FAILED",
            "orderId": order.get("orderId"),
            "step": "orchestrator",
            "error": str(exc),
        }


@app.activity_trigger(input_name="order")
def validate_order_activity(order: dict) -> dict:
    return validate_order(order)


@app.activity_trigger(input_name="order")
def process_payment_activity(order: dict) -> dict:
    return process_payment(order)


@app.activity_trigger(input_name="order")
def send_notification_activity(order: dict) -> dict:
    return send_notification(order)
