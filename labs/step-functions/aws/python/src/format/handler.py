from datetime import datetime, timezone


def lambda_handler(event, context):
    v = event["viacep"]
    return {
        "status": "SUCCESS",
        "cep": event["cep"],
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
    }
