# GCP — Cloud Workflows + Cloud Functions (busca CEP)

Conta, projeto e deploy detalhado: [../CONTAS-E-DEPLOY.md](../CONTAS-E-DEPLOY.md#gcp)

| Linguagem | Pasta | Runtime |
|-----------|-------|---------|
| Python | [python/](python/) | python312 |
| Node.js | [nodejs/](nodejs/) | nodejs20 |

## Deploy functions (Python — exemplo)

```bash
export PROJECT_ID=seu-projeto
export REGION=southamerica-east1

cd python
for fn in validate fetch format; do
  gcloud functions deploy cep-${fn} \
    --gen2 --runtime=python312 --region=$REGION \
    --source=functions/${fn} \
    --entry-point=handler \
    --trigger-http --allow-unauthenticated
done
```

## Deploy functions (Node.js)

```bash
cd nodejs
for fn in validate fetch format; do
  gcloud functions deploy cep-${fn} \
    --gen2 --runtime=nodejs20 --region=$REGION \
    --source=functions/${fn} \
    --entry-point=handler \
    --trigger-http --allow-unauthenticated
done
```

## Workflow

Substitua URLs em `workflow.yaml` pelas URIs das functions e:

```bash
gcloud workflows deploy cep-lookup --source=workflow.yaml --location=$REGION
gcloud workflows run cep-lookup --location=$REGION \
  --data="$(cat ../spec/events/cep-lookup.json)"
```

Lab sem OIDC: use `workflow-local.yaml.example` (HTTP sem auth).
