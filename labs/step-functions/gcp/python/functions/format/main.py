from datetime import datetime, timezone

import functions_framework


@functions_framework.http
def handler(request):
    payload = request.get_json(silent=True) or {}
    v = payload.get("viacep")
    if not v:
        return ({"error": "viacep ausente"}, 400)

    return (
        {
            "status": "SUCCESS",
            "cep": payload.get("cep"),
            "address": {
                "street": v.get("logradouro", ""),
                "complement": v.get("complemento", ""),
                "neighborhood": v.get("bairro", ""),
                "city": v.get("localidade", ""),
                "state": v.get("uf", ""),
                "ibge": v.get("ibge", ""),
            },
            "source": "viacep",
            "fetchedAt": datetime.now(timezone.utc).isoformat(),
        },
        200,
    )
