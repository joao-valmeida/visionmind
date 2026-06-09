# Contas nas clouds e deploy da app Busca CEP

Guia para alunos da pós: criar conta (ou usar créditos gratuitos), configurar CLI e publicar o workflow **ValidateCEP → FetchCEP → FormatResponse** em **AWS**, **Azure** e **GCP**.

App: [spec/workflow.md](spec/workflow.md)  
Payload de teste: [spec/events/cep-lookup.json](spec/events/cep-lookup.json)

| Cloud | Orquestração | Pastas |
|-------|----------------|--------|
| AWS | Step Functions + Lambda | [aws/python](aws/python/), [aws/nodejs](aws/nodejs/) |
| Azure | Durable Functions | [azure/python](azure/python/), [azure/nodejs](azure/nodejs/) |
| GCP | Cloud Workflows + Cloud Functions | [gcp/python](gcp/python/), [gcp/nodejs](gcp/nodejs/) |

---

## Ferramentas (instalar antes)

| Ferramenta | AWS | Azure | GCP |
|------------|-----|-------|-----|
| CLI | [AWS CLI v2](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) | [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) | [gcloud](https://cloud.google.com/sdk/docs/install) |
| Deploy | [SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) | [Azure Functions Core Tools v4](https://learn.microsoft.com/azure/azure-functions/functions-run-local) | (incluído no gcloud) |
| Runtime local | Python 3.12 ou Node 20 | idem | idem |

---

## AWS

### 1. Criar conta

1. Acesse [https://aws.amazon.com](https://aws.amazon.com) → **Criar uma conta da AWS**.
2. E-mail, senha, nome da conta e contato.
3. Cartão de crédito (cobrança só após free tier; alunos podem usar conta dedicada ao lab).
4. Plano de suporte: **Básico (gratuito)**.
5. Ative **MFA** no usuário root (recomendado).

**Free tier (resumo):** Lambda, Step Functions e CloudWatch têm camada gratuita mensal — suficiente para este lab. Detalhes: [AWS Free Tier](https://aws.amazon.com/free/).

### 2. Usuário IAM (não use root no dia a dia)

1. Console → **IAM** → **Users** → **Create user** (ex.: `serverless-lab`).
2. Permissões: anexe `AdministratorAccess` **apenas em conta de lab**; em produção use políticas mínimas.
3. **Security credentials** → **Create access key** → CLI → guarde `Access Key ID` e `Secret Access Key`.

### 3. Configurar CLI

```bash
aws configure
# AWS Access Key ID: ...
# AWS Secret Access Key: ...
# Default region name: us-east-1   (ou sa-east-1)
# Default output format: json

aws sts get-caller-identity
```

### 4. Deploy — Python

```bash
cd labs/step-functions/aws/python

sam build
sam deploy --guided
```

Sugestões no `--guided`:

| Pergunta | Valor sugerido |
|----------|----------------|
| Stack Name | `serverless-unifor-cep` |
| Region | `us-east-1` ou `sa-east-1` |
| Confirm changes | Y |
| Allow SAM CLI IAM role creation | Y |

Anote o output **`StateMachineArn`**.

### 5. Deploy — Node.js

```bash
cd labs/step-functions/aws/nodejs
sam build
sam deploy --guided
```

(Use outro stack name se já deployou Python, ex.: `serverless-unifor-cep-node`.)

### 6. Testar

```bash
aws stepfunctions start-execution \
  --state-machine-arn "arn:aws:states:REGION:ACCOUNT:stateMachine:..." \
  --input file://../../spec/events/cep-lookup.json
```

Ver resultado:

```bash
aws stepfunctions describe-execution --execution-arn "<execution-arn-from-output>"
```

Console: **Step Functions** → state machine → **Executions**.

### 7. Limpar (evitar custo)

```bash
sam delete --stack-name serverless-unifor-cep
```

---

## Azure

### 1. Criar conta

1. [https://azure.microsoft.com/free](https://azure.microsoft.com/free) → **Comece gratuitamente**.
2. Conta Microsoft, telefone, cartão (validação; crédito inicial para novos assinantes).
3. Portal: [https://portal.azure.com](https://portal.azure.com).

**Estudantes:** verifique [Azure for Students](https://azure.microsoft.com/free/students/) (sem cartão em alguns programas).

### 2. Login na CLI

```bash
az login
az account list -o table
az account set --subscription "<SUBSCRIPTION_ID>"
az account show
```

### 3. Recursos para Durable Functions

```bash
export RG=rg-serverless-unifor
export LOC=brazilsouth
export STORAGE=stserverlessunifor$RANDOM
export FUNCAPP=fa-serverless-unifor-cep

az group create -n $RG -l $LOC

az storage account create -n $STORAGE -g $RG -l $LOC --sku Standard_LRS

az functionapp create \
  -g $RG -n $FUNCAPP -l $LOC \
  --storage-account $STORAGE \
  --consumption-plan-location $LOC \
  --runtime python \
  --functions-version 4 \
  --os-type Linux
```

Para **Node.js**, troque `--runtime python` por `--runtime node --runtime-version 20`.

### 4. Deploy — Python

```bash
cd labs/step-functions/azure/python

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp local.settings.json.example local.settings.json
# Edite local.settings.json se não usar Azurite

func azure functionapp publish $FUNCAPP
```

### 5. Deploy — Node.js

```bash
cd labs/step-functions/azure/nodejs
npm install
func azure functionapp publish $FUNCAPP
```

(Se a Function App foi criada com runtime Python, crie outra com `--runtime node` ou recrie a app.)

### 6. Testar

URL no portal: **Function App** → **Functions** → trigger HTTP `cep`.

```bash
curl -X POST "https://${FUNCAPP}.azurewebsites.net/api/cep?code=<FUNCTION_KEY>" \
  -H "Content-Type: application/json" \
  -d @../../spec/events/cep-lookup.json
```

A chave (`code`) está em **Function** → **Get Function Url** ou **App keys**.

Resposta inicial retorna URL de status da orquestração Durable; consulte até `runtimeStatus` = `Completed`.

### 7. Teste local (sem conta na nuvem)

```bash
cd labs/step-functions/azure/python   # ou nodejs
func start
curl -X POST http://localhost:7071/api/cep \
  -H "Content-Type: application/json" \
  -d @../spec/events/cep-lookup.json
```

### 8. Limpar

```bash
az group delete -n $RG --yes --no-wait
```

---

## GCP

### 1. Criar conta / projeto

1. [https://cloud.google.com](https://cloud.google.com) → **Get started for free**.
2. Conta Google, faturamento (crédito trial para contas novas).
3. Console: [https://console.cloud.google.com](https://console.cloud.google.com).
4. **IAM & Admin** → **Create project** (ex.: `serverless-unifor-lab`).
5. Vincule **billing account** ao projeto.

**Estudantes:** [Google Cloud Skills Boost / créditos educacionais](https://cloud.google.com/edu) quando disponível na instituição.

### 2. Configurar gcloud

```bash
gcloud auth login
gcloud config set project SEU_PROJECT_ID
gcloud config set compute/region southamerica-east1

gcloud auth application-default login
```

### 3. Habilitar APIs

```bash
gcloud services enable \
  cloudfunctions.googleapis.com \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  workflows.googleapis.com \
  workflowexecutions.googleapis.com
```

### 4. Deploy — Python (3 functions + workflow)

```bash
export PROJECT_ID=$(gcloud config get-value project)
export REGION=southamerica-east1

cd labs/step-functions/gcp/python

for fn in validate fetch format; do
  gcloud functions deploy cep-${fn} \
    --gen2 \
    --runtime=python312 \
    --region=$REGION \
    --source=functions/${fn} \
    --entry-point=handler \
    --trigger-http \
    --allow-unauthenticated
done
```

Anote as **URIs** de cada function:

```bash
gcloud functions describe cep-validate --gen2 --region=$REGION --format='value(serviceConfig.uri)'
gcloud functions describe cep-fetch    --gen2 --region=$REGION --format='value(serviceConfig.uri)'
gcloud functions describe cep-format   --gen2 --region=$REGION --format='value(serviceConfig.uri)'
```

Edite `workflow.yaml` — substitua `VALIDATE_URL`, `FETCH_URL`, `FORMAT_URL` pelas URIs.

```bash
gcloud workflows deploy cep-lookup \
  --source=workflow.yaml \
  --location=$REGION
```

### 5. Deploy — Node.js

```bash
cd labs/step-functions/gcp/nodejs

for fn in validate fetch format; do
  gcloud functions deploy cep-${fn} \
    --gen2 \
    --runtime=nodejs20 \
    --region=$REGION \
    --source=functions/${fn} \
    --entry-point=handler \
    --trigger-http \
    --allow-unauthenticated
done
```

Atualize `workflow.yaml` com as novas URLs e rode `gcloud workflows deploy` de novo.

Dica: copie [workflow-local.yaml.example](gcp/python/workflow-local.yaml.example) como base.

### 6. Testar

```bash
gcloud workflows run cep-lookup \
  --location=$REGION \
  --data="$(cat ../../spec/events/cep-lookup.json)"
```

Ver execução:

```bash
gcloud workflows executions list cep-lookup --location=$REGION
gcloud workflows executions describe <EXECUTION_ID> \
  --workflow=cep-lookup --location=$REGION
```

### 7. Limpar

```bash
gcloud workflows delete cep-lookup --location=$REGION --quiet
for fn in validate fetch format; do
  gcloud functions delete cep-${fn} --gen2 --region=$REGION --quiet
done
```

---

## Checklist por aluno

- [ ] Conta criada na cloud escolhida
- [ ] CLI instalada e autenticada
- [ ] Deploy concluído (Python **ou** Node — depois repetir na outra linguagem)
- [ ] Teste com CEP `01001-000` → endereço em São Paulo
- [ ] Teste com CEP inválido `123` → erro em ValidateCEP
- [ ] (Opcional) Mesmo fluxo em segunda cloud e comparar README de cada pasta

---

## Custos e boas práticas

| Prática | Motivo |
|---------|--------|
| Usar região próxima (`sa-east-1`, `brazilsouth`, `southamerica-east1`) | Latência menor para ViaCEP |
| Apagar stacks/resource groups ao fim do mês | Evitar cobrança após free tier |
| Não commitar access keys | Use `aws configure`, `az login`, `gcloud auth` |
| Lab: `--allow-unauthenticated` só em GCP Functions de teste | Em produção use IAM/OIDC |

---

## Links úteis

- AWS SAM: [docs.aws.amazon.com/serverless-application-model](https://docs.aws.amazon.com/serverless-application-model/)
- Azure Durable Functions: [learn.microsoft.com/azure/azure-functions/durable](https://learn.microsoft.com/azure/azure-functions/durable/durable-functions-overview)
- GCP Workflows: [cloud.google.com/workflows/docs](https://cloud.google.com/workflows/docs)
