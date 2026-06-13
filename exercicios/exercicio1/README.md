# Exercício 1: API CRUD Serverless

## Objetivo
Criar uma API REST básica para gerenciar itens em um banco de dados NoSQL.

## Arquitetura
- **AWS**: API Gateway + Lambda (Python) + DynamoDB.
- **GCP**: Cloud Function (HTTP) + Firestore.
- **Azure**: Azure Function (HTTP Trigger) + CosmosDB.

---

## 🛠 Configuração de Credenciais e CLI

Antes de iniciar, escolha sua nuvem e configure o ambiente:

### 1. AWS
*   **Usuário:** Vá ao console IAM, crie um usuário (ex: `aluno-serverless`) e anexe a política `AdministratorAccess`.
*   **Credenciais:** Em "Security Credentials", gere uma **Access Key** e **Secret Key**.
*   **Instalação do SAM CLI:** Para simplificar o deploy e upload de código, instale o AWS SAM CLI: [Instruções de Instalação](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
*   **Configuração:**
    ```bash
    aws configure
    ```
*   **Deploy (AWS SAM):**
    ```bash
    cd aws
    sam deploy --guided
    ```
    *(O modo guided criará o bucket S3 necessário e fará o upload do código automaticamente)*.

### 2. Google Cloud (GCP)
*   **Usuário:** Crie um projeto no console GCP e garanta que seu usuário tenha a role `Owner` ou `Editor`.
*   **CLI:** Instale o `gcloud sdk` e autentique:
    ```bash
    gcloud auth login
    gcloud config set project SEU_PROJECT_ID
    ```
*   **Deploy (Terraform):**
    ```bash
    cd gcp
    terraform init
    terraform apply
    ```

### 3. Azure
*   **Usuário:** Crie uma conta no portal Azure. Seu usuário deve ter a role `Contributor` ou `Owner` na Subscription.
*   **CLI:** Instale o `azure-cli` e autentique:
    ```bash
    az login
    ```
*   **Deploy (Terraform):**
    ```bash
    cd azure
    terraform init
    terraform apply
    ```

---

## 📝 Tarefas do Exercício
1. Analise o código da função em cada cloud.
2. Explore os arquivos de infraestrutura (Serverless Framework, CloudFormation, Terraform).
3. Faça o deploy em sua conta de preferência usando os comandos acima.
4. Teste os endpoints POST e GET (as URLs serão exibidas no output do deploy).
