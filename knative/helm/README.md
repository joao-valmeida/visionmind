# Helm — Knative (Operator CRs)

Este chart aplica os CRs gerenciados pelo **Knative Operator**. Não substitui a instalação do Operator.

## Pré-requisito

```bash
export KNATIVE_VERSION=1.17.0
kubectl apply -f https://github.com/knative/operator/releases/download/knative-v${KNATIVE_VERSION}/operator.yaml
```

## Instalar

```bash
helm upgrade --install knative-serving . \
  -n knative-serving --create-namespace \
  -f values.yaml
```

## Parâmetros principais

| Value | Descrição |
|-------|-----------|
| `serving.version` | Versão do Knative Serving |
| `serving.istio.enabled` | Usa `net-istio` (requer Istio no cluster) |
| `serving.istio.knativeIngressGateway.selector` | Label do gateway Istio ingress |
| `eventing.enabled` | Instala Knative Eventing |

## Verificar

```bash
kubectl get knativeserving -n knative-serving
kubectl get pods -n knative-serving
```

## GitOps (opcional)

Este chart é para o lab da pós. Em produção, adapte values (versão, HA, domínio) ao ambiente da turma.
