# AWS — Step Functions + Lambda

## Arquitetura

```
API Gateway (opcional) ou CLI
        ↓
Step Functions (Standard)
        ↓
Lambda: ValidateOrder → ProcessPayment → SendNotification
```

## Pré-requisitos

- AWS CLI configurado
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- Python 3.12

## Deploy

```bash
cd labs/step-functions/aws
sam build
sam deploy --guided
```

Parâmetros sugeridos no `--guided`:

- Stack name: `serverless-unifor-order`
- Region: `us-east-1` (ou sa-east-1)

## Executar

```bash
aws stepfunctions start-execution \
  --state-machine-arn "$(aws cloudformation describe-stacks \
    --stack-name serverless-unifor-order \
    --query 'Stacks[0].Outputs[?OutputKey==`StateMachineArn`].OutputValue' \
    --output text)" \
  --input file://../spec/events/order-created.json
```

Falha simulada:

```bash
aws stepfunctions start-execution \
  --state-machine-arn "<ARN>" \
  --input '{"orderId":"X","customerEmail":"a@b.com","amount":10,"simulateFailure":true}'
```

## Arquivos

| Arquivo | Descrição |
|---------|-----------|
| `template.yaml` | SAM — Lambdas + State Machine |
| `state-machine.asl.json` | Definição ASL |
| `src/*/handler.py` | Código das três funções |

## Exercício

1. Adicionar **Retry** em `ProcessPayment` (2 tentativas, backoff).
2. Exportar diagrama no console Step Functions e comparar com Azure/GCP.
