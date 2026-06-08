# Knative + Istio

Este Helm habilita `spec.ingress.istio` no `KnativeServing`, usando o gateway de ingress do lab (`istio: ingress`).

Instale Istio antes: [../../cluster/istio/README.md](../../cluster/istio/README.md).

## O que o chart configura

- **knative-ingress-gateway** — tráfego externo (selector `istio: ingress`)
- **knative-local-gateway** — tráfego interno (mesmo selector no lab Kind)

Valores em `helm/values.yaml` → `serving.istio`.

## Domínio dos KServices

### Opção A — ConfigMap `config-domain` (lab)

Após Serving Ready:

```bash
kubectl patch configmap config-domain -n knative-serving --type merge -p '{
  "data": {
    "serverless.lab": ""
  }
}'
```

URL: `http://hello.default.serverless.lab` (com Host header ou `/etc/hosts`).

### Opção B — DomainMapping

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
```

Acesse via Gateway Istio + host configurado.

## HTTPS (opcional)

Em lab Kind, HTTP na porta mapeada costuma bastar. Para TLS, adicione listener 443 no Gateway Istio e certificado (cert-manager ou auto-assinado).

## Troubleshooting

| Sintoma | Verificação |
|---------|-------------|
| 404 no host | `kubectl get ksvc`, `kubectl get gateway,virtualservice -A` |
| Pod não sobe | `kubectl describe ksvc`, eventos de webhook |
| Escala não zera | `kubectl get podautoscaler` no namespace do KService |
