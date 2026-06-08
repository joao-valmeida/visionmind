# Kind — cluster de lab (Kubernetes 1.36)

Cluster **Kind** com **1 control-plane** e **3 workers**, API e HTTP Istio expostos no host.

## Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/)
- [Kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installation) v0.27+
- [kubectl](https://kubernetes.io/docs/tasks/tools/)

```bash
kind version
docker info
```

## 1. Ajustar IP e portas

Edite [kind-config.yaml](kind-config.yaml) ou use `sed` (ver [../README.md](../README.md)):

| Campo | Placeholder | Exemplo |
|-------|-------------|---------|
| `listenAddress` | `IP-A-ALTERAR` | `192.168.56.10` ou `0.0.0.0` |
| API Server | `PORTA-KUBE-API-A-ALTERAR` | `6443` |
| Istio HTTP | `PORTA-ISTIO-HTTP-A-ALTERAR` | `8080` |

> **Nota:** `listenAddress` precisa ser um IP válido no host (não deixe literal `IP-A-ALTERAR` ao criar o cluster).

## 2. Criar cluster

```bash
cd Serverless-Pos-Unifor/cluster/kind

kind create cluster --name serverless-unifor --config kind-config.yaml
```

## 3. Verificar

```bash
kubectl cluster-info
kubectl get nodes -o wide
# Esperado: 1 control-plane + 3 workers, todos Ready
kubectl get nodes --show-labels | grep ingress-ready
```

O label `ingress-ready=true` no control-plane prepara o mapeamento da porta HTTP para o Istio (instalação na etapa seguinte).

## 4. Kubeconfig remoto (opcional)

Se expôs a API em `IP-A-ALTERAR:PORTA-KUBE-API-A-ALTERAR`, ajuste o server no kubeconfig:

```bash
# Copie ~/.kube/config para sua máquina e altere:
# server: https://127.0.0.1:PORTA
# para:
# server: https://IP-A-ALTERAR:PORTA-KUBE-API-A-ALTERAR
```

Obtenha o certificado CA embutido no kubeconfig gerado pelo Kind (`certificate-authority-data`).

## 5. Destruir

```bash
kind delete cluster --name serverless-unifor
```

## Topologia

```
Host (IP-A-ALTERAR)
  ├── :PORTA-KUBE-API-A-ALTERAR  → control-plane:6443 (API)
  ├── :PORTA-ISTIO-HTTP-A-ALTERAR → control-plane:80 (mapeado p/ Istio depois)
  └── Docker
        ├── serverless-unifor-control-plane
        └── serverless-unifor-worker (×3)
```

## Troubleshooting

| Problema | Solução |
|----------|---------|
| Porta em uso | Troque `PORTA-*-A-ALTERAR` |
| Imagem 1.36 não encontrada | `docker pull kindest/node:v1.36.0` |
| Workers NotReady | Aguarde 1–2 min; `docker logs` no container do nó |

Próximo passo: [Instalar Istio](../istio/README.md).
