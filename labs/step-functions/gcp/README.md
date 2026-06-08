# GCP — Cloud Workflows + Cloud Functions (Gen2)

Mesma app de pedido usando **Workflows** (YAML) chamando **HTTP** Cloud Functions.

## Arquitetura

```
gcloud workflows run
        ↓
workflow.yaml (sequência + retry)
        ↓
HTTPS → Cloud Functions: validate | payment | notify
```

## Pré-requisitos

- `gcloud` CLI autenticado
- Projeto GCP com APIs: Workflows, Cloud Functions, Cloud Build

```bash
gcloud services enable workflows.googleapis.com cloudfunctions.googleapis.com run.googleapis.com
```

## Deploy das funções

Ajuste `PROJECT_ID` e `REGION`:

```bash
export PROJECT_ID=seu-projeto
export REGION=southamerica-east1

cd labs/step-functions/gcp

for fn in validate payment notify; do
  gcloud functions deploy order-${fn} \
    --gen2 --runtime=python312 --region=$REGION \
    --source=functions/${fn} \
    --entry-point=handler \
    --trigger-http --allow-unauthenticated
done
```

Anote as URLs retornadas (`uri`).

## Deploy do workflow

Edite `workflow.yaml` substituindo os placeholders `VALIDATE_URL`, `PAYMENT_URL`, `NOTIFY_URL` pelas URLs das functions.

```bash
gcloud workflows deploy order-processing \
  --source=workflow.yaml \
  --location=$REGION
```

## Executar

```bash
gcloud workflows run order-processing \
  --location=$REGION \
  --data="$(cat ../spec/events/order-created.json)"
```

## Arquivos

| Arquivo | Descrição |
|---------|-----------|
| `workflow.yaml` | Definição Cloud Workflows |
| `functions/*/main.py` | Lógica (espelho das Lambdas AWS) |

## Comparar com AWS/Azure

| Aspecto | GCP Workflows |
|---------|----------------|
| Sintaxe | YAML declarativo |
| Compute | Cloud Functions Gen2 (HTTP) |
| Estado | Gerenciado pelo Workflows |

## Exercício

Trocar `--allow-unauthenticated` por IAM (OIDC) e usar `auth` no passo HTTP do workflow.
