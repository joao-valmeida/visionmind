# Planejamento de aulas — Serverless

## Módulo 1 — Conceitos

| Aula | Conteúdo | Material |
|------|----------|----------|
| 1.1 | FaaS vs PaaS vs containers; cold start; stateless | Slides |
| 1.2 | Event-driven, HTTP serverless, APIs externas (ViaCEP) | `labs/step-functions/spec/workflow.md` |
| 1.3 | Comparativo AWS / Azure / GCP (tabela de serviços) | README dos labs |

## Módulo 2 — Workflows (mesma app, 3 clouds)

**Guia de contas + deploy:** [labs/step-functions/CONTAS-E-DEPLOY.md](labs/step-functions/CONTAS-E-DEPLOY.md)

| Aula | Cloud | Lab |
|------|-------|-----|
| 2.1 | **AWS** — Lambda + Step Functions (ASL) | [labs/step-functions/aws/](labs/step-functions/aws/) |
| 2.2 | **Azure** — Durable Functions (orquestrador + activities) | [labs/step-functions/azure/](labs/step-functions/azure/) |
| 2.3 | **GCP** — Cloud Workflows + Cloud Functions | [labs/step-functions/gcp/](labs/step-functions/gcp/) |
| 2.4 | Discussão: retries, DLQ, observabilidade, custo | Comparar os 3 READMEs |

**Objetivo:** aluno implementa a mesma **busca de CEP** em Python e Node.js e documenta diferenças (sintaxe, deploy, billing).

## Módulo 3 — Knative no Kubernetes

| Aula | Conteúdo | Material |
|------|----------|----------|
| 3.1 | Kind + Istio (lab local) | [cluster/](cluster/) |
| 3.2 | Serving, KService, escala automática | [knative/README.md](knative/README.md) |
| 3.3 | Instalação: Operator + Helm | [knative/docs/02-instalacao-operator.md](knative/docs/02-instalacao-operator.md) |
| 3.4 | Primeiro deploy + tráfego canário | [knative/docs/04-primeiro-kservice.md](knative/docs/04-primeiro-kservice.md) |
| 3.5 | (Opcional) Eventing | [knative/docs/06-eventing.md](knative/docs/06-eventing.md) |

## Módulo 4 — Integração e produção

| Aula | Tema |
|------|------|
| 4.1 | API Gateway / Ingress / mTLS |
| 4.2 | CI/CD serverless (GitHub Actions, SAM, Terraform Bicep, etc.) |
| 4.3 | Monitoramento: Uptime, traces, métricas de cold start |

## Entregáveis sugeridos (alunos)

1. Deploy do workflow de CEP em **uma** cloud + linguagem (Python ou Node) + diagrama.
2. Deploy de um **KService** no cluster com autoscale.
3. Relatório curto: quando usar Knative vs Lambda vs Step Functions.

## Ordem recomendada de preparação (professor)

1. Validar labs AWS/Azure/GCP em conta de demonstração.
2. Subir cluster Kind + Istio (`cluster/`).
3. Instalar Knative no cluster de lab (seguir `knative/helm`).
