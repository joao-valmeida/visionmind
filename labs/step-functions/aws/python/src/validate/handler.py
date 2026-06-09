import re


def lambda_handler(event, context):
    raw = str(event.get("cep", "")).strip()
    digits = re.sub(r"\D", "", raw)

    if len(digits) != 8:
        raise ValueError(f"CEP inválido: '{raw}' — esperado 8 dígitos")

    return {
        "cep": digits,
        "normalized": True,
        "simulateFailure": bool(event.get("simulateFailure", False)),
    }
