import azure.durable_functions as df
import azure.functions as func

from activities import fetch_cep, format_response, validate_cep

app = df.DFApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.route(route="cep", methods=["POST"])
@app.durable_client_input(client_name="client")
async def cep_http(req: func.HttpRequest, client):
    try:
        body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    instance_id = await client.start_new("cep_orchestrator", None, body)
    return client.create_check_status_response(req, instance_id)


@app.orchestration_trigger(context_name="context")
def cep_orchestrator(context: df.DurableOrchestrationContext):
    payload = context.get_input()
    try:
        validated = yield context.call_activity("validate_cep_activity", payload)
        fetched = yield context.call_activity("fetch_cep_activity", validated)
        return yield context.call_activity("format_response_activity", fetched)
    except Exception as exc:
        return {
            "status": "FAILED",
            "cep": (payload or {}).get("cep", ""),
            "step": "orchestrator",
            "error": str(exc),
        }


@app.activity_trigger(input_name="payload")
def validate_cep_activity(payload: dict) -> dict:
    return validate_cep(payload)


@app.activity_trigger(input_name="payload")
def fetch_cep_activity(payload: dict) -> dict:
    return fetch_cep(payload)


@app.activity_trigger(input_name="payload")
def format_response_activity(payload: dict) -> dict:
    return format_response(payload)
