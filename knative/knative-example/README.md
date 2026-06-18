# Knative no Kind (Guia Completo)

Este guia documenta como o Knative Serving foi instalado no seu cluster Kind e como testar aplicações serverless.

## 1. Como a Instalação foi Feita

Se precisar replicar em outro cluster, estes foram os passos executados:

### Passo A: Instalar CRDs e Componentes do Serving
```bash
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.14.0/serving-crds.yaml
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.14.0/serving-core.yaml
```

### Passo B: Instalar a Camada de Rede (Kourier)
```bash
kubectl apply -f https://github.com/knative/net-kourier/releases/download/knative-v1.14.0/kourier.yaml

# Configurar o Knative para usar o Kourier como Ingress padrão
kubectl patch configmap/config-network \
  --namespace knative-serving \
  --type merge \
  --patch '{"data":{"ingress-class":"kourier.ingress.networking.knative.dev"}}'
```

### Passo C: Configurar o Domínio (sslip.io)
Para o Kind, configuramos manualmente o domínio para resolver para o IP local:
```bash
kubectl patch configmap/config-domain \
  --namespace knative-serving \
  --type merge \
  --patch '{"data":{"127.0.0.1.sslip.io":""}}'
```

---

## 2. Como Testar a Aplicação de Exemplo

### Passo 1: Subir a aplicação
```bash
kubectl apply -f hello-world.yaml
```

### Passo 2: Acessar pelo Navegador (Port-Forward)
O Knative usa Virtual Hosts. Para o navegador conseguir acessar, a URL deve bater com o domínio configurado.

1. **Inicie o port-forward** (em um terminal separado):
   ```bash
   kubectl port-forward -n kourier-system svc/kourier 8080:80
   ```

2. **Abra no navegador**:
   Acesse: [http://hello.default.127.0.0.1.sslip.io:8080](http://hello.default.127.0.0.1.sslip.io:8080)

   *Nota: Se você acessar via `http://localhost:8080`, receberá um erro **404**, pois o Knative não reconhece o host "localhost".*

---

## 3. O Ciclo de Vida Serverless (O que acontece por baixo dos panos)

O Knative possui um componente chamado **Autoscaler** que monitora o tráfego.

### Scale-to-Zero (Escalando para Zero)
Se a sua aplicação ficar aproximadamente **60 segundos** (padrão) sem receber requisições, o Knative irá terminar os Pods para economizar recursos. Você verá o status dos Pods mudar para `Terminating` e depois sumirem.

### O "Cold Start" (Despertando o Pod)
Quando você faz uma requisição no browser e não há Pods ativos:

1. **Requisição retida:** O **Activator** (componente do Knative) recebe a requisição e a segura "em espera".
2. **Sinal de Escalonamento:** O Activator avisa o Autoscaler que chegou tráfego.
3. **Criação do Pod:** O Kubernetes inicia um novo Pod da sua aplicação.
4. **Encaminhamento:** Assim que o Pod passa no *readiness probe* (fica pronto), o Activator repassa a requisição que estava segurando para o novo Pod.
5. **Resposta:** Você recebe o "Hello Knative!" no navegador.

**Resultado:** A primeira requisição após o Pod estar zerado demora alguns segundos a mais (o tempo de subida do container). As requisições seguintes serão instantâneas enquanto o Pod estiver ativo.
