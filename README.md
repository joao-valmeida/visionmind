# Serverless — Pós-Graduação Unifor

Material de planejamento e laboratórios para aulas de **serverless** em múltiplas plataformas.

## Estrutura

```
Serverless-Pos-Unifor/
  PLANNING.md                 # Roteiro de aulas
  knative/                    # Kubernetes serverless (Helm + docs)
  labs/step-functions/        # Mesma app, 3 clouds
    spec/                     # Contrato comum do workflow
    aws/                      # Step Functions + Lambda
    azure/                    # Durable Functions
    gcp/                      # Cloud Workflows + Cloud Functions
```

## Laboratórios

| Tema | Pasta | Foco |
|------|-------|------|
| Knative no K8s | [knative/](knative/) | KService, escala 0→N, Istio |
| Workflow multi-cloud | [labs/step-functions/](labs/step-functions/) | Mesmo fluxo de pedido em AWS, Azure e GCP |

## App canônica (step functions)

**Processamento de pedido** — três etapas com tratamento de falha:

1. `ValidateOrder` — valida payload
2. `ProcessPayment` — simula cobrança (pode falhar de propósito)
3. `SendNotification` — confirma ao cliente

Ver [labs/step-functions/spec/workflow.md](labs/step-functions/spec/workflow.md).

## Pré-requisitos gerais

- Conta/créditos em AWS, Azure e GCP (ou sandbox da turma)
- Cluster Kubernetes com Istio (para Knative) — ver [knative/docs/01-pre-requisitos.md](knative/docs/01-pre-requisitos.md)
- `kubectl`, `helm`, CLI das clouds (`aws`, `az`, `gcloud`)
