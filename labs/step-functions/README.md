# Lab — Mesma app em 3 clouds (workflows)

Uma única aplicação de negócio implementada com orquestração serverless em **AWS**, **Azure** e **GCP**.

## App: Processamento de pedido

```
[Pedido] → ValidateOrder → ProcessPayment → SendNotification → [OK]
                ↓ falha              ↓ falha
            FailState            FailState
```

| Etapa | Responsabilidade |
|-------|------------------|
| **ValidateOrder** | JSON válido, `orderId`, `amount` > 0, `customerEmail` |
| **ProcessPayment** | Simula cobrança; falha se `amount > 10000` ou `simulateFailure: true` |
| **SendNotification** | Retorna confirmação (log / e-mail simulado) |

Contrato completo: [spec/workflow.md](spec/workflow.md)  
Payload de exemplo: [spec/events/order-created.json](spec/events/order-created.json)

## Projetos

| Cloud | Serviço de orquestração | Pasta |
|-------|-------------------------|-------|
| AWS | Step Functions + Lambda | [aws/](aws/) |
| Azure | Durable Functions | [azure/](azure/) |
| GCP | Cloud Workflows + Cloud Functions | [gcp/](gcp/) |

## Como usar na aula

1. Leia o `spec/workflow.md` com a turma (contrato único).
2. Demonstre **uma** cloud ao vivo (sugestão: AWS).
3. Alunos replicam o fluxo nas outras duas e preenchem a tabela comparativa no README de cada pasta.
4. Teste com payload válido e com `simulateFailure: true`.

## Tabela comparativa (preencher com alunos)

| Critério | AWS | Azure | GCP |
|----------|-----|-------|-----|
| Linguagem do workflow | ASL (JSON) | C#/Python/Java | YAML |
| Unidade de compute | Lambda | Function | Cloud Function |
| Retry nativo | Sim (ASL) | Sim (policies) | Sim (`retry`) |
| Observabilidade | CloudWatch | App Insights | Cloud Logging |
| Deploy deste lab | SAM | `func azure functionapp` | `gcloud workflows deploy` |
