# Serverless — Pós-Graduação Unifor

Material de planejamento, teoria e laboratórios para o curso de **Serverless Computing**.

## Estrutura do Repositório

```text
Serverless-Pos-Unifor/
├── Apostila_Serverless_UNIFOR.docx    # Material teórico de apoio
├── PLANNING.md                        # Roteiro detalhado das aulas
├── Plano_de_Ensino_Serverless.docx    # Plano pedagógico
├── Slides_Serverless_UNIFOR.pptx      # Slides das aulas
├── cluster/                           # Setup de Kind + Istio (lab local)
├── knative/                           # Kubernetes Serverless (Helm + documentação)
├── exercicios/                        # Laboratórios práticos por cloud
│   ├── exercicio1/                    # API CRUD (AWS/GCP/Azure)
│   ├── exercicio2/                    # Event-Driven (S3/Storage triggers)
│   └── exercicio3/                    # Filas, VPC e DB Relacional
├── trabalhos/                         # Projetos de referência e avaliação
│   ├── produto1-ecotrack/             # Calculadora de Carbono (API)
│   ├── produto2-swiftpay/             # Processador de Pagamentos (SQS)
│   └── produto3-visionmind/           # Análise de Imagens (Eventos)
└── labs/                              # Workflows complexos (em desenvolvimento)
```

## Conteúdo Programático

### 1. Infraestrutura Local e Knative
Foco em entender a abstração de containers para serverless no Kubernetes.
- [cluster/](cluster/): Provisionamento de cluster `kind` com `istio`.
- [knative/](knative/): Deploy de KServices, escala 0→N e roteamento de tráfego.

### 2. Laboratórios em Cloud (AWS, Azure, GCP)
Exercícios práticos para dominar os principais provedores de nuvem.
- **[Exercicio 1](exercicios/exercicio1/):** CRUD Serverless com API Gateway e NoSQL.
- **[Exercicio 2](exercicios/exercicio2/):** Arquiteturas orientadas a eventos (Storage triggers).
- **[Exercicio 3](exercicios/exercicio3/):** Integração com VPC, Filas (SQS/PubSub) e Bancos de Dados Relacionais.

### 3. Projetos de Referência (Trabalhos)
Aplicações "canônicas" simulando startups reais:
- **EcoTrack:** API de cálculos de sustentabilidade.
- **SwiftPay:** Worker assíncrono para processamento de transações.
- **VisionMind:** Pipeline de inteligência artificial disparado por upload de arquivos.

## Pré-requisitos Gerais

- Contas ativas com créditos em AWS, Azure e GCP.
- Ferramentas locais: `kubectl`, `helm`, `kind`, `docker`.
- CLI das nuvens instaladas e configuradas (`aws`, `az`, `gcloud`).
- `terraform` e `aws-sam-cli` para os deploys automatizados.
