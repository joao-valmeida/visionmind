# Knative — Kubernetes serverless

Knative **Serving** expõe containers com escala automática (incluindo **scale-to-zero**) e roteamento HTTP. Este material usa **Istio** como camada de rede (compatível com o cluster de infra da turma/lab).

## Visão rápida

```
Cliente → Istio Gateway → Knative Activator/Queue-Proxy → Pod(s) da revisão
                ↑
         KService (CRD)
```

## Instalação (ordem)

| Passo | O quê | Onde |
|-------|--------|------|
| 1 | Pré-requisitos (K8s, Istio, DNS) | [docs/01-pre-requisitos.md](docs/01-pre-requisitos.md) |
| 2 | Knative **Operator** (uma vez no cluster) | [docs/02-instalacao-operator.md](docs/02-instalacao-operator.md) |
| 3 | **Helm** — `KnativeServing` (+ Eventing opcional) | [helm/](helm/) |
| 4 | Istio + domínio | [docs/03-istio.md](docs/03-istio.md) |
| 5 | Primeiro `KService` | [docs/04-primeiro-kservice.md](docs/04-primeiro-kservice.md) |

## Helm deste repo

```bash
# Após instalar o Operator (passo 2)
helm upgrade --install knative-serving ./helm \
  -n knative-serving --create-namespace \
  -f helm/values.yaml
```

O chart **não** instala o Operator — apenas os CRs `KnativeServing` / `KnativeEventing` e namespaces. Ver [helm/README.md](helm/README.md).

## Versão padrão

- Knative **1.17.x** (ajuste em `helm/values.yaml` → `serving.version`)

## Referências

- [Knative docs](https://knative.dev/docs/)
- [Knative Operator](https://knative.dev/docs/install/operator/knative-with-operators/)
