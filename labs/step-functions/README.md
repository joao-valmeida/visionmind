# Lab — Busca de CEP em 3 clouds (Python + Node.js)

Uma única aplicação — **consulta de CEP via ViaCEP** — orquestrada em **AWS**, **Azure** e **GCP**, cada uma com implementação em **Python** e **Node.js**.

**Comece aqui:** [CONTAS-E-DEPLOY.md](CONTAS-E-DEPLOY.md) — criar contas, configurar CLI e deploy passo a passo em cada cloud.

## Fluxo

```
[CEP] → ValidateCEP → FetchCEP (ViaCEP) → FormatResponse → [endereço]
              ↓ falha           ↓ falha
           Failed            Failed
```

| Etapa | Responsabilidade |
|-------|------------------|
| **ValidateCEP** | Normaliza e valida 8 dígitos |
| **FetchCEP** | HTTP GET em `viacep.com.br` |
| **FormatResponse** | Resposta padronizada para a turma |

Contrato: [spec/workflow.md](spec/workflow.md)  
Payload: [spec/events/cep-lookup.json](spec/events/cep-lookup.json)

## Estrutura por cloud

```
aws/
  python/     # Lambda Python + Step Functions
  nodejs/     # Lambda Node 20 + Step Functions
azure/
  python/     # Durable Functions (Python)
  nodejs/     # Durable Functions (Node)
gcp/
  python/     # Cloud Functions + Workflows
  nodejs/     # Cloud Functions + Workflows
```

## Como usar na aula

1. Leia `spec/workflow.md` (contrato único).
2. Demonstre **uma** cloud + **uma** linguagem (sugestão: AWS Python).
3. Alunos replicam nas outras clouds e/ou trocam Python ↔ Node.
4. Teste CEP válido (`01001-000`), inválido (`123`) e `simulateFailure: true`.

## Tabela comparativa

| Critério | AWS | Azure | GCP |
|----------|-----|-------|-----|
| Orquestração | Step Functions (ASL) | Durable Functions | Cloud Workflows |
| Python | `aws/python/` | `azure/python/` | `gcp/python/` |
| Node.js | `aws/nodejs/` | `azure/nodejs/` | `gcp/nodejs/` |
| Deploy Python | `sam deploy` | `func start` / publish | `gcloud functions deploy` |
| Deploy Node | `sam deploy` | `npm start` / publish | `gcloud functions deploy` |
