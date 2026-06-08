# Instalação do Knative Operator

O **Operator** gerencia o ciclo de vida do Knative Serving/Eventing via CRDs. Instale **uma vez** por cluster (fora do Helm deste chart).

## 1. Instalar CRDs e Operator

Escolha a versão alinhada ao `helm/values.yaml` (`serving.version`).

```bash
export KNATIVE_VERSION=1.17.0

kubectl apply -f https://github.com/knative/operator/releases/download/knative-v${KNATIVE_VERSION}/operator.yaml
```

Aguarde:

```bash
kubectl wait --for=condition=Ready pod -l app=knative-operator -n knative-operator --timeout=300s
```

## 2. Verificar

```bash
kubectl get pods -n knative-operator
kubectl api-resources | grep knative
```

Deve listar `KnativeServing`, `KnativeEventing` em `operator.knative.dev`.

## 3. Aplicar Helm (Serving)

```bash
cd Serverless-Pos-Unifor/knative
helm upgrade --install knative-serving ./helm \
  -n knative-serving --create-namespace \
  -f helm/values.yaml
```

## 4. Aguardar Serving pronto

```bash
kubectl wait --for=condition=Ready knativeserving/knative-serving -n knative-serving --timeout=600s
kubectl get pods -n knative-serving
```

## Atualizar versão

1. Ajuste `serving.version` no `values.yaml`.
2. `helm upgrade` do chart.
3. O Operator reconcilia os manifests da nova versão.

## Desinstalar (lab)

```bash
helm uninstall knative-serving -n knative-serving
kubectl delete knativeserving knative-serving -n knative-serving --ignore-not-found
kubectl delete knativeeventing knative-eventing -n knative-eventing --ignore-not-found
kubectl delete -f https://github.com/knative/operator/releases/download/knative-v${KNATIVE_VERSION}/operator.yaml
```
