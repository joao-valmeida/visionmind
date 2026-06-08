# Pré-requisitos — Knative

## Cluster Kubernetes

| Item | Mínimo | Lab PagueMenos (referência) |
|------|--------|-----------------------------|
| Versão K8s | 1.28+ | 1.35.x |
| CNI | Qualquer suportado | Calico/Cilium/etc. |
| Storage | Opcional (só se app precisar PVC) | nfs-client |
| CPU nos workers | 2+ vCPU livres para Knative + Istio | 3 workers |

## Istio (rede Knative)

Knative com **`net-istio`** exige Istio instalado **antes** do Serving.

No cluster de infra:

- `istiod` em `istio-system`
- Gateway ingress com label `istio: ingress` em `istio-ingress`
- Certificado TLS wildcard (opcional para HTTPS em KServices)

Sem Istio, altere `helm/values.yaml` → `serving.ingress.class: kourier` e instale Kourier (não coberto neste material).

## Ferramentas locais

```bash
kubectl version --client
helm version
```

## Capacidade do cluster

Knative adiciona componentes em namespaces `knative-serving`, `istio-system` (sidecars):

- **controller**, **activator**, **autoscaler**, **webhook**

Reserve ~500m CPU e ~512Mi RAM além do que já consome o control plane.

## DNS (produção / lab com URL fixa)

Configure um wildcard ou host por app, por exemplo:

- `*.serverless.pmenos.com.br` → IP do Istio ingress

No `config-domain` (ConfigMap gerenciado pelo Knative) o domínio padrão pode ser alterado após install — ver [03-istio.md](03-istio.md).

## Checklist antes de instalar

- [ ] `kubectl get nodes` — todos Ready
- [ ] `kubectl get pods -n istio-system` — istiod Running
- [ ] `kubectl get pods -n istio-ingress` — gateway Running
- [ ] Sem outro ingress controller conflitando na porta 80/443 do NodePort/LB
