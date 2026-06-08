# Knative + Istio

Este Helm habilita `spec.ingress.istio` no `KnativeServing`, usando o gateway de ingress já existente (`istio: ingress`).

## O que o chart configura

- **knative-ingress-gateway** — tráfego externo (mesmo selector do `infra-gateway`)
- **knative-local-gateway** — tráfego interno mesh (opcional em labs pequenos; pode usar o mesmo selector)

Valores em `helm/values.yaml` → `serving.istio`.

## Domínio dos KServices

Por padrão Knative gera URLs `*.svc.cluster.local` internas. Para URL pública:

### Opção A — ConfigMap `config-domain` (recomendado em lab)

Após Serving Ready:

```bash
kubectl patch configmap config-domain -n knative-serving --type merge -p '{
  "data": {
    "serverless.pmenos.com.br": ""
  }
}'
```

Novos KServices passam a usar `https://<kservice>.<namespace>.serverless.pmenos.com.br`.

### Opção B — Integrar com `platform/istio-routing` (infra core)

Adicione hosts wildcard no Gateway e um VirtualService por KService, ou use **DomainMapping** (Knative 1.8+):

```yaml
apiVersion: serving.knative.dev/v1beta1
kind: DomainMapping
metadata:
  name: hello
  namespace: default
spec:
  ref:
    name: hello
    kind: Service
    apiVersion: serving.knative.dev/v1
  url: https://hello-serverless.pmenos.com.br
```

## HTTPS

- Terminação TLS no **Istio Gateway** (cert-manager wildcard), igual Argo/Harbor.
- Knative fala HTTP com o sidecar na porta do container.

## Troubleshooting

| Sintoma | Verificação |
|---------|-------------|
| 404 no host | `kubectl get ksvc`, `kubectl get virtualservice -A` |
| Pod não sobe | `kubectl describe ksvc`, eventos de webhook |
| Escala não zera | `kubectl get podautoscaler` no namespace do KService |
