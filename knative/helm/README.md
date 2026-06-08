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

## Integração GitOps (opcional)

Para colocar no `TEC-RT-K8S-INFRA-CORE`, copie o chart para `platform/knative/` e adicione Application no `root-app` com sync **manual** (igual Istio).
