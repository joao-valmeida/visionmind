# Exercício 3: Filas, VPC e Banco de Dados Relacional

## Objetivo
Implementar um padrão de processamento em segundo plano com persistência em banco de dados relacional dentro de uma rede privada (VPC).

## Arquitetura
- **AWS**: API Gateway -> SQS -> Lambda (VPC) -> Aurora Postgres Serverless.
- **GCP**: Cloud Pub/Sub -> Cloud Function (VPC Connector) -> Cloud SQL (Postgres).
- **Azure**: Service Bus -> Azure Function (VNet Integration) -> Azure Database for PostgreSQL.

---

## 🛠 Configuração de Credenciais e CLI

### 1. AWS
*   **Instalação do SAM CLI:** [Instruções de Instalação](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
*   **Deploy (AWS SAM):**
    ```bash
    cd aws
    sam deploy --guided
    ```

### 2. Google Cloud (GCP)
*   **Deploy (Terraform):**
    ```bash
    cd gcp
    terraform init
    terraform apply
    ```

### 3. Azure
*   **Deploy (Terraform):**
    ```bash
    cd azure
    terraform init
    terraform apply
    ```

---

## 📝 Tarefas do Exercício
1. Entenda como a função acessa o banco de dados sem exposição pública (uso de subnets privadas e VPC Connectors).
2. Simule o envio de mensagens para a fila/tópico.
3. Verifique a persistência dos dados no banco via query SQL ou logs da função.
