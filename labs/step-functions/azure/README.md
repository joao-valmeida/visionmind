# Azure — Durable Functions (equivalente a Step Functions)

Orquestração com **Durable Functions** (modelo fan-out/fan-in e function chaining). Mesma lógica de negócio que AWS/GCP.

## Arquitetura

```
HTTP trigger (order_http)
        ↓
Orchestrator (order_orchestrator) — determinístico
        ↓
Activity: validate_order → process_payment → send_notification
```

## Pré-requisitos

- Azure Functions Core Tools v4
- Python 3.11+
- Conta Azure + Storage Account (connection string)

```bash
pip install azure-functions azure-functions-durable
```

## Estrutura local

```bash
cd labs/step-functions/azure
func start
```

## Deploy

```bash
az login
az group create -n rg-serverless-unifor -l brazilsouth
az storage account create -n stserverlessunifor -g rg-serverless-unifor -l brazilsouth --sku Standard_LRS
func azure functionapp publish fa-serverless-unifor-order
```

Configure `AzureWebJobsStorage` na Function App com a connection string do storage.

## Testar

```bash
curl -X POST "http://localhost:7071/api/orders" \
  -H "Content-Type: application/json" \
  -d @../spec/events/order-created.json
```

Status da orquestração:

```bash
curl "http://localhost:7071/runtime/webhooks/durabletask/instances/<instanceId>"
```

## Arquivos

| Arquivo | Papel |
|---------|-------|
| `function_app.py` | Orchestrator + HTTP starter |
| `activities.py` | Validate, Payment, Notify |
| `host.json` | Durable Task extension |

## Comparar com AWS

| AWS | Azure |
|-----|-------|
| ASL JSON | Código Python (`yield context.call_activity`) |
| Step Functions console | Durable Functions monitor / Application Insights |
| Lambda | Activity Function |

## Exercício

Implementar **timer** de timeout na orquestração (`context.create_timer`) e comparar com `TimeoutSeconds` do ASL.
