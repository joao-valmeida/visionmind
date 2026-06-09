import json
import re

import functions_framework


@functions_framework.http
def handler(request):
    payload = request.get_json(silent=True) or {}
    raw = str(payload.get("cep", "")).strip()
    digits = re.sub(r"\D", "", raw)

    if len(digits) != 8:
        return ({"error": f"CEP inválido: '{raw}' — esperado 8 dígitos"}, 400)

    return (
        {
            "cep": digits,
            "normalized": True,
            "simulateFailure": bool(payload.get("simulateFailure", False)),
        },
        200,
    )
