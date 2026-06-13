# Exercício 2: Arquitetura Orientada a Eventos

## Objetivo
Processar eventos de upload de arquivos de forma assíncrona.

## Arquitetura
- **AWS**: S3 -> EventBridge -> Lambda (Python).
- **GCP**: Cloud Storage -> Eventarc -> Cloud Function.
- **Azure**: Blob Storage -> Event Grid -> Azure Function.

---

## 🛠 Configuração de Credenciais e CLI

### 1. AWS
*   **Instalação do SAM CLI:** [Instruções de Instalação](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
*   **Deploy (Opção A - AWS SAM):**
    ```bash
    cd aws
    sam deploy --guided
    ```
*   **Deploy (Opção B - Serverless Framework):**
    ```bash
    cd aws
    npm install -g serverless
    serverless deploy
    ```

### 2. Google Cloud (GCP)
*   **Autenticação:** `gcloud auth application-default login`
*   **Deploy (Terraform):**
    ```bash
    cd gcp
    terraform init
    terraform apply
    ```

### 3. Azure
*   **Autenticação:** `az login`
*   **Deploy (Terraform):**
    ```bash
    cd azure
    terraform init
    terraform apply
    ```

---

## 📝 Tarefas do Exercício
1. Configure o gatilho (trigger) para que a função seja disparada em cada novo arquivo.
2. Faça o upload de um arquivo para o bucket/container criado e acompanhe os logs.
3. Observe como os metadados do evento (nome do arquivo, tamanho) chegam até a função.
