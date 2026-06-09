import json
import re
import urllib.request
from datetime import datetime, timezone


def validate_cep(payload: dict) -> dict:
    raw = str(payload.get("cep", "")).strip()
    digits = re.sub(r"\D", "", raw)
    if len(digits) != 8:
        raise ValueError(f"CEP inválido: '{raw}' — esperado 8 dígitos")
    return {
        "cep": digits,
        "normalized": True,
        "simulateFailure": bool(payload.get("simulateFailure", False)),
    }


def fetch_cep(payload: dict) -> dict:
    if payload.get("simulateFailure"):
        raise RuntimeError("Falha simulada em FetchCEP")

    cep = payload["cep"]
    url = f"https://viacep.com.br/ws/{cep}/json/"
    with urllib.request.urlopen(url, timeout=10) as resp:
        data = json.loads(resp.read().decode())

    if data.get("erro"):
        raise ValueError(f"CEP não encontrado: {cep}")

    return {**payload, "viacep": data}


def format_response(payload: dict) -> dict:
    v = payload["viacep"]
    return {
        "status": "SUCCESS",
        "cep": payload["cep"],
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
