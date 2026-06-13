# Planejamento de aulas — Serverless

## Módulo 1 — Conceitos

| Aula | Conteúdo | Material |
|------|----------|----------|
| 1.1 | FaaS vs PaaS vs containers; cold start; stateless | Slides |
| 1.2 | Event-driven, HTTP serverless, APIs externas (ViaCEP) | `labs/step-functions/spec/workflow.md` |
| 1.3 | Comparativo AWS / Azure / GCP (tabela de serviços) | README dos labs |

## Módulo 2 — Laboratórios Cloud (AWS, Azure, GCP)

**Objetivo:** O aluno implementa padrões fundamentais em cada provedor para entender as diferenças de sintaxe, infraestrutura (Terraform/SAM) e billing.

| Aula | Tema | Pasta |
|------|------|-------|
| 2.1 | API CRUD (API Gateway + Functions + NoSQL) | [exercicios/exercicio1/](exercicios/exercicio1/) |
| 2.2 | Event-Driven (Storage Triggers + Event Bridge) | [exercicios/exercicio2/](exercicios/exercicio2/) |
| 2.3 | Mensageria e VPC (Filas + RDBMS Privado) | [exercicios/exercicio3/](exercicios/exercicio3/) |
| 2.4 | Discussão: Retries, Observabilidade e Custos | Comparar deploys |

## Módulo 3 — Projetos Práticos (Trabalhos)

Cenários reais de startups para aplicação dos conceitos aprendidos.

- **EcoTrack:** Foco em APIs síncronas e Cache. [trabalhos/produto1-ecotrack/](trabalhos/produto1-ecotrack/)
- **SwiftPay:** Foco em processamento em fila e alta escala. [trabalhos/produto2-swiftpay/](trabalhos/produto2-swiftpay/)
- **VisionMind:** Foco em pipelines de processamento de mídia. [trabalhos/produto3-visionmind/](trabalhos/produto3-visionmind/)

## Módulo 4 — Knative no Kubernetes

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
