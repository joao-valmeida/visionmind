# Guia de Configuração de Identidade (Azure e GCP)

Este guia explica como permitir que o GitHub Actions faça deploy de forma segura na Azure e GCP usando identidades federadas (OIDC), eliminando a necessidade de senhas ou chaves permanentes.

---

## 1. Azure (OIDC via Service Principal)

### Passo 1: Criar o App Registration
1. No Portal Azure, vá em **Microsoft Entra ID** > **App registrations** > **New registration**.
2. Nomeie como `github-actions-serverless`.

### Passo 2: Configurar a Credencial Federada
1. No App Registration criado, vá em **Certificates & secrets** > **Federated credentials** > **Add credential**.
2. Selecione **GitHub Actions deploying Azure resources**.
3. Preencha seu usuário e repositório.
4. Em **Entity type**, escolha `Environment`, `Branch`, `Pull request` ou `Tag`.

### Passo 3: Atribuir Permissões
1. Vá na sua **Subscription** > **Access Control (IAM)** > **Add role assignment**.
2. Atribua o papel de **Contributor** ao App Registration criado.

### Passo 4: Configurar Secrets no GitHub
Adicione as seguintes secrets no seu repositório:
* `AZURE_CLIENT_ID`: Application (client) ID do App Registration.
* `AZURE_TENANT_ID`: Directory (tenant) ID.
* `AZURE_SUBSCRIPTION_ID`: ID da sua Subscription.

---

## 2. GCP (Workload Identity Federation)

### Passo 1: Criar o Workload Identity Pool
No Cloud Shell:
```bash
gcloud iam workload-identity-pools create "github-pool" \
    --project="SEU_PROJETO" \
    --location="global" \
    --display-name="GitHub Actions Pool"
```

### Passo 2: Criar o Provider
```bash
gcloud iam workload-identity-pools providers create-oidc "github-provider" \
    --project="SEU_PROJETO" \
    --location="global" \
    --workload-identity-pool="github-pool" \
    --display-name="GitHub Provider" \
    --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository" \
    --issuer-uri="https://token.actions.githubusercontent.com"
```

### Passo 3: Conectar à Service Account
Crie uma Service Account e dê permissão para o GitHub usá-la:
```bash
gcloud iam service-accounts add-iam-policy-binding "SUA_SERVICE_ACCOUNT@SEU_PROJETO.iam.gserviceaccount.com" \
    --project="SEU_PROJETO" \
    --role="roles/iam.workloadIdentityUser" \
    --member="principalSet://iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/attribute.repository/USUARIO/REPO"
```

### Passo 4: Configurar Secrets no GitHub
* `GCP_PROJECT_ID`: ID do seu projeto GCP.
* `GCP_SERVICE_ACCOUNT`: Email da Service Account criada.
* `GCP_WORKLOAD_IDENTITY_PROVIDER`: O caminho completo do provider (ex: `projects/12345/locations/global/workloadIdentityPools/github-pool/providers/github-provider`).

---

## Como usar os Workflows
Agora você verá dois novos workflows no GitHub: **"Exercicio 1 Azure Pipeline"** e **"Exercicio 1 GCP Pipeline"**. Eles funcionam de forma idêntica ao da AWS, garantindo que os testes passem antes do deploy.
