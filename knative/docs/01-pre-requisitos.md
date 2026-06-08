# Pré-requisitos — Knative

## Cluster Kubernetes

| Item | Mínimo | Lab (Kind deste repo) |
|------|--------|------------------------|
| Versão K8s | 1.28+ | **1.36** ([cluster/kind](../cluster/kind/)) |
| Istio | Obrigatório (`net-istio`) | [cluster/istio](../cluster/istio/) |
| Nós | 1+ control-plane | 1 CP + 3 workers |
| CPU | ~2 vCPU livres | Docker host da turma |

## Istio (rede Knative)

Knative com **`net-istio`** exige Istio instalado **antes** do Serving.

Siga [cluster/istio/README.md](../cluster/istio/README.md):

- `istiod` em `istio-system`
- Gateway ingress com label `istio: ingress` em `istio-ingress`

Sem Istio, altere `helm/values.yaml` → use Kourier (não documentado neste curso).

## Ferramentas locais

```bash
kubectl version --client
helm version
kind version
docker version
```

## DNS (opcional em lab)

Com Kind, acesse serviços via `http://IP-A-ALTERAR:PORTA-ISTIO-HTTP-A-ALTERAR` ou configure `/etc/hosts`:

```text
IP-A-ALTERAR  hello.default.serverless.lab
```

Para domínio Knative, patch `config-domain` — ver [03-istio.md](03-istio.md).

## Checklist antes de instalar Knative

- [ ] `kubectl get nodes` — 4 nós Ready
- [ ] `kubectl get pods -n istio-system` — istiod Running
- [ ] `kubectl get pods -n istio-ingress` — gateway Running
- [ ] Teste httpbin do README Istio passou
