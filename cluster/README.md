# Cluster local — Kind + Istio

Ambiente de laboratório da pós-graduação (**independente** de qualquer repo corporativo).

```
cluster/
  kind/
    kind-config.yaml    # 1 control-plane + 3 workers, K8s 1.36
    README.md
  istio/
    README.md           # Instalação Istio (istioctl)
    values-ingress.yaml # Gateway ingress (NodePort / Kind)
```

## Ordem

1. [Kind — criar cluster](kind/README.md)
2. [Istio — instalar](istio/README.md)
3. [Knative](../knative/README.md) (usa Istio como rede)

## Placeholders no `kind-config.yaml`

Antes de `kind create cluster`, substitua no YAML:

| Placeholder | Uso |
|-------------|-----|
| `IP-A-ALTERAR` | IP da VM/host onde o Kind roda (ex. `192.168.56.10`) |
| `PORTA-KUBE-API-A-ALTERAR` | Porta da API em `networking.apiServerPort` (ex. `6443`) — **não** duplicar em `extraPortMappings` |
| `PORTA-ISTIO-HTTP-A-ALTERAR` | Porta HTTP Istio em `extraPortMappings` (ex. `8080`) |

```bash
# Linux/macOS — exemplo
export LAB_IP=192.168.56.10
export KUBE_API_PORT=6443
export ISTIO_HTTP_PORT=8080

sed -e "s/IP-A-ALTERAR/${LAB_IP}/g" \
    -e "s/PORTA-KUBE-API-A-ALTERAR/${KUBE_API_PORT}/g" \
    -e "s/PORTA-ISTIO-HTTP-A-ALTERAR/${ISTIO_HTTP_PORT}/g" \
    kind/kind-config.yaml | kind create cluster --config=-
```

Ou edite o arquivo manualmente.
