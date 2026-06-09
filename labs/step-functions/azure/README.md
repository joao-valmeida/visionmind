# Azure — Durable Functions (busca CEP)

Conta, recursos e deploy detalhado: [../CONTAS-E-DEPLOY.md](../CONTAS-E-DEPLOY.md#azure)

| Linguagem | Pasta | Comando local |
|-----------|-------|---------------|
| Python | [python/](python/) | `func start` |
| Node.js | [nodejs/](nodejs/) | `npm start` |

## Fluxo

```
POST /api/cep  →  orchestrator  →  validate → fetch → format
```

## Python

```bash
cd python
pip install -r requirements.txt
func start
curl -X POST http://localhost:7071/api/cep \
  -H "Content-Type: application/json" \
  -d @../spec/events/cep-lookup.json
```

## Node.js

```bash
cd nodejs
npm install
npm start
curl -X POST http://localhost:7071/api/cep \
  -H "Content-Type: application/json" \
  -d @../spec/events/cep-lookup.json
```

## Deploy

```bash
func azure functionapp publish <FUNCTION_APP_NAME>
```

Configure `AzureWebJobsStorage` na Function App.
