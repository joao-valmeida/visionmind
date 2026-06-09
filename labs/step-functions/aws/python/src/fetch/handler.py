import json
import urllib.request


def lambda_handler(event, context):
    if event.get("simulateFailure"):
        raise RuntimeError("Falha simulada em FetchCEP")

    cep = event["cep"]
    url = f"https://viacep.com.br/ws/{cep}/json/"

    with urllib.request.urlopen(url, timeout=10) as resp:
        data = json.loads(resp.read().decode())

    if data.get("erro"):
        raise ValueError(f"CEP não encontrado: {cep}")

    return {**event, "viacep": data}
