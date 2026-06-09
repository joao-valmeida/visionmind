import json
import urllib.request

import functions_framework


@functions_framework.http
def handler(request):
    payload = request.get_json(silent=True) or {}

    if payload.get("simulateFailure"):
        return ({"error": "Falha simulada em FetchCEP"}, 500)

    cep = payload.get("cep")
    if not cep:
        return ({"error": "CEP ausente"}, 400)

    url = f"https://viacep.com.br/ws/{cep}/json/"
    with urllib.request.urlopen(url, timeout=10) as resp:
        data = json.loads(resp.read().decode())

    if data.get("erro"):
        return ({"error": f"CEP não encontrado: {cep}"}, 404)

    return ({**payload, "viacep": data}, 200)
