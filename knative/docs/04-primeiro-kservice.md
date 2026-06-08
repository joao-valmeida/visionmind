# Primeiro KService

## Deploy de exemplo

```bash
kubectl apply -f - <<'EOF'
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: hello
  namespace: default
spec:
  template:
    spec:
      containers:
        - image: ghcr.io/knative/helloworld-go:latest
          ports:
            - containerPort: 8080
          env:
            - name: TARGET
              value: "Serverless Unifor"
EOF
```

## Verificar

```bash
kubectl get ksvc hello
kubectl get pods -l serving.knative.dev/service=hello
```

URL (com `config-domain` = `serverless.lab` e entrada no `/etc/hosts`):

```text
http://hello.default.serverless.lab
```

Teste (Kind — ajuste IP/porta do [kind-config.yaml](../../cluster/kind/kind-config.yaml)):

```bash
curl -s "http://IP-A-ALTERAR:PORTA-ISTIO-HTTP-A-ALTERAR" \
  -H "Host: hello.default.serverless.lab"
```

## Autoscale (scale to zero)

```bash
# aguarde ~60s sem tráfego
kubectl get pods -l serving.knative.dev/service=hello
# 0 pods — cold start na próxima requisição
curl -s "http://IP-A-ALTERAR:PORTA-ISTIO-HTTP-A-ALTERAR" \
  -H "Host: hello.default.serverless.lab"
kubectl get pods -l serving.knative.dev/service=hello
```

## Tráfego canário (duas revisões)

```bash
kubectl apply -f - <<'EOF'
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: hello
  namespace: default
spec:
  template:
    metadata:
      name: hello-v2
    spec:
      containers:
        - image: ghcr.io/knative/helloworld-go:latest
          env:
            - name: TARGET
              value: "Revisão 2"
EOF

kubectl patch ksvc hello -n default --type=json -p '[
  {"op":"replace","path":"/spec/traffic","value":[
    {"percent":50,"revisionName":"hello-v1"},
    {"percent":50,"revisionName":"hello-v2"}
  ]}
]'
```

Ajuste `revisionName` conforme `kubectl get revisions`.

## Exercício para alunos

1. Deploy do helloworld.
2. Medir tempo de cold start (primeira request após idle).
3. Publicar imagem no registry da turma (Docker Hub ou registry compartilhado) e apontar o KService para ela.
