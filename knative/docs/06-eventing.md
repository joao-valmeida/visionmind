# Knative Eventing (opcional)

Habilite no Helm: `eventing.enabled: true` e `helm upgrade`.

## Conceitos

- **Broker** — hub de eventos (Kafka, RabbitMQ ou in-memory em dev)
- **Trigger** — filtro que encaminha eventos para um KService
- **Source** — gera eventos (Ping, ApiServer, etc.)

## Exemplo Ping → KService

```bash
kubectl apply -f - <<'EOF'
apiVersion: eventing.knative.dev/v1
kind: Broker
metadata:
  name: default
  namespace: default
---
apiVersion: sources.knative.dev/v1
kind: PingSource
metadata:
  name: ping-hello
  namespace: default
spec:
  schedule: "*/1 * * * *"
  contentType: application/json
  data: '{"message":"tick"}'
  sink:
    ref:
      apiVersion: eventing.knative.dev/v1
      kind: Broker
      name: default
---
apiVersion: eventing.knative.dev/v1
kind: Trigger
metadata:
  name: hello-trigger
  namespace: default
spec:
  broker: default
  filter:
    attributes:
      type: dev.knative.sources.ping
  subscriber:
    ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: hello
EOF
```

Em produção prefira broker com persistência (Kafka). O chart default usa o broker in-memory do Knative para lab.
