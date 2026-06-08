# Istio — instalação no cluster Kind

Istio como **camada de rede** para Knative e labs de ingress. Testado com o cluster [Kind](../kind/README.md).

## Pré-requisitos

- Cluster Kind `serverless-unifor` Running
- `kubectl get nodes` — 4 nós Ready

## 1. Instalar istioctl

```bash
# Linux — exemplo Istio 1.27.x (ajuste versão se necessário)
export ISTIO_VERSION=1.27.0
curl -L https://istio.io/downloadIstio | ISTIO_VERSION=$ISTIO_VERSION sh -
export PATH="$PWD/istio-$ISTIO_VERSION/bin:$PATH"
istioctl version
```

Documentação: [istio.io/latest/docs/setup/getting-started](https://istio.io/latest/docs/setup/getting-started/)

## 2. Instalar control plane (istiod)

Perfil **default** — suficiente para lab + Knative:

```bash
istioctl install -y --set profile=default
```

Verificar:

```bash
kubectl get pods -n istio-system
kubectl wait --for=condition=Ready pod -l app=istiod -n istio-system --timeout=300s
```

## 3. Instalar ingress gateway (Helm)

Repositório oficial:

```bash
helm repo add istio https://istio-release.storage.googleapis.com/charts
helm repo update

helm upgrade --install istio-ingress istio/gateway \
  -n istio-ingress --create-namespace \
  -f values-ingress.yaml
```

O arquivo [values-ingress.yaml](values-ingress.yaml) define:

- Label `istio: ingress` (selector usado pelo Knative neste curso)
- Service `NodePort` (compatível com Kind + `extraPortMappings` porta 80)

Verificar:

```bash
kubectl get svc -n istio-ingress
kubectl get pods -n istio-ingress -l istio=ingress
```

## 4. Teste HTTP via Kind

Se no [kind-config.yaml](../kind/kind-config.yaml) você mapeou:

- host `IP-A-ALTERAR:PORTA-ISTIO-HTTP-A-ALTERAR` → container `:80`

Instale um app de teste:

```bash
kubectl create namespace demo
kubectl label namespace demo istio-injection=enabled --overwrite

kubectl apply -n demo -f - <<'EOF'
apiVersion: v1
kind: Service
metadata:
  name: httpbin
spec:
  selector:
    app: httpbin
  ports:
    - port: 8000
      name: http
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: httpbin
spec:
  replicas: 1
  selector:
    matchLabels:
      app: httpbin
  template:
    metadata:
      labels:
        app: httpbin
    spec:
      containers:
        - name: httpbin
          image: docker.io/kennethreitz/httpbin
          ports:
            - containerPort: 80
EOF
```

Gateway + VirtualService mínimos:

```bash
kubectl apply -f - <<'EOF'
apiVersion: networking.istio.io/v1
kind: Gateway
metadata:
  name: lab-gateway
  namespace: istio-ingress
spec:
  selector:
    istio: ingress
  servers:
    - port:
        number: 80
        name: http
        protocol: HTTP
      hosts:
        - "*"
---
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: httpbin
  namespace: demo
spec:
  hosts:
    - "*"
  gateways:
    - istio-ingress/lab-gateway
  http:
    - route:
        - destination:
            host: httpbin
            port:
              number: 8000
EOF
```

Teste (substitua IP e porta):

```bash
curl -s "http://IP-A-ALTERAR:PORTA-ISTIO-HTTP-A-ALTERAR/get" -H "Host: httpbin.demo.local"
```

Resposta JSON do httpbin confirma Istio + Kind OK.

## 5. Integração com Knative

Após Istio pronto, siga [../../knative/docs/02-instalacao-operator.md](../../knative/docs/02-instalacao-operator.md).

No Helm Knative (`knative/helm/values.yaml`), confirme:

```yaml
serving:
  istio:
    knativeIngressGateway:
      selector:
        istio: ingress
```

## 6. Desinstalar (lab)

```bash
helm uninstall istio-ingress -n istio-ingress
istioctl uninstall -y --purge
kubectl delete namespace istio-ingress --ignore-not-found
```

## Referência rápida

| Componente | Namespace | Selector / label |
|------------|-----------|------------------|
| istiod | `istio-system` | — |
| Ingress gateway | `istio-ingress` | `istio: ingress` |

## Alternativa: só istioctl (sem Helm gateway)

```bash
istioctl install -y --set profile=demo \
  --set values.gateways.istio-ingressgateway.type=NodePort
```

Para Knative, o gateway precisa do label `istio: ingress` — prefira o passo 3 com `values-ingress.yaml`.
