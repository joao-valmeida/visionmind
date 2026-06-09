# AWS — Step Functions + Lambda (busca CEP)

Conta, IAM e deploy detalhado: [../CONTAS-E-DEPLOY.md](../CONTAS-E-DEPLOY.md#aws)

| Linguagem | Pasta | Runtime |
|-----------|-------|---------|
| Python | [python/](python/) | python3.12 |
| Node.js | [nodejs/](nodejs/) | nodejs20.x |

## Deploy (escolha uma pasta)

```bash
cd python   # ou nodejs
sam build
sam deploy --guided
```

Stack sugerida: `serverless-unifor-cep`

## Executar

```bash
aws stepfunctions start-execution \
  --state-machine-arn "<ARN>" \
  --input file://../spec/events/cep-lookup.json
```

CEP não encontrado:

```bash
aws stepfunctions start-execution \
  --state-machine-arn "<ARN>" \
  --input '{"cep":"00000-000"}'
```

## Arquivos

- `template.yaml` — SAM (3 Lambdas + State Machine)
- `state-machine.asl.json` — ASL
- `src/validate`, `src/fetch`, `src/format` — handlers
