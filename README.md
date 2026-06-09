# Serverless — Pós-Graduação Unifor

Material de planejamento e laboratórios para aulas de **serverless** em múltiplas plataformas.

## Estrutura

```
Serverless-Pos-Unifor/
  PLANNING.md                 # Roteiro de aulas
  cluster/                    # Kind + Istio (lab local)
  knative/                    # Kubernetes serverless (Helm + docs)
  labs/step-functions/        # Mesma app, 3 clouds
```

## Laboratórios

| Tema | Pasta | Foco |
|------|-------|------|
| Knative no K8s | [knative/](knative/) | KService, escala 0→N, Istio |
| Workflow multi-cloud | [labs/step-functions/](labs/step-functions/) | Busca CEP em AWS, Azure e GCP |

## App canônica (step functions)

**Busca de CEP** (ViaCEP) — três etapas:

1. `ValidateCEP` — normaliza e valida 8 dígitos
2. `FetchCEP` — consulta `viacep.com.br`
3. `FormatResponse` — endereço padronizado

Implementações em **Python** e **Node.js** em cada cloud (AWS, Azure, GCP).

Ver [labs/step-functions/spec/workflow.md](labs/step-functions/spec/workflow.md).

**Contas e deploy nas clouds:** [labs/step-functions/CONTAS-E-DEPLOY.md](labs/step-functions/CONTAS-E-DEPLOY.md)

## Pré-requisitos gerais

- Conta/créditos em AWS, Azure e GCP — ver guia acima
- Cluster local: [cluster/kind](cluster/kind/) + [cluster/istio](cluster/istio/) (Kind 1.36 + Istio)
- `kubectl`, `helm`, `kind`, CLI das clouds (`aws`, `az`, `gcloud`)
