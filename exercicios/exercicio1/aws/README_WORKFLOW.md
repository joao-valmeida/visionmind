# Guia de Workflow e Configuração AWS OIDC

Este documento explica o funcionamento da pipeline de CI/CD para o **Exercicio 1 (AWS)** e como configurar a integração segura entre o GitHub Actions e a AWS usando OIDC (OpenID Connect).

---

## 1. O Workflow (.github/workflows/exercicio1-aws.yml)

A pipeline é acionada manualmente via **Workflow Dispatch** e possui três estágios principais:

### Estágios:
1.  **Run Python Tests:**
    *   Instala dependências de teste (`pytest`, `moto`).
    *   Executa testes unitários simulando o DynamoDB localmente.
    *   **Bloqueia o deploy** se os testes falharem.
2.  **Deploy to AWS:**
    *   Faz o build da aplicação usando `sam build`.
    *   Realiza o deploy para a stack `teste-exercicio1` na região `us-east-2`.
3.  **Delete AWS Stack:**
    *   Remove completamente a stack e todos os recursos associados da AWS.

---

## 2. Configurando o Identity Provider (OIDC) na AWS

Para que o GitHub Actions acesse sua conta AWS sem usar chaves de acesso (Access Keys) permanentes, configuramos um **Identity Provider**.

### Passo 1: Criar o Identity Provider
1.  Acesse o console do **IAM** > **Identity providers** > **Add provider**.
2.  Selecione **OpenID Connect**.
3.  **Provider URL:** `https://token.actions.githubusercontent.com` (Clique em "Get thumbprint").
4.  **Audience:** `sts.amazonaws.com`.
5.  Clique em **Add provider**.

---

## 3. Configurando a IAM Role

Agora você precisa criar uma Role que o GitHub possa "assumir".

### Passo 1: Criar a Role
1.  No IAM, vá em **Roles** > **Create role**.
2.  Selecione **Custom trust policy** e cole o seguinte JSON (ajuste com seu usuário/repo):

```json
{
  "Version": "2012-10-10",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::960583973883:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:<SEU_USUARIO>/<SEU_REPOSITORIO>:*"
        },
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        }
      }
    }
  ]
}
```

### Passo 2: Adicionar Permissões
Atribua as permissões necessárias para o SAM operar (ex: `AdministratorAccess` para fins de estudo, ou permissões granulares de CloudFormation, S3, Lambda, IAM e DynamoDB).

### Passo 3: Nome da Role
Nomeie a role como `github-identity-provider` (conforme configurado no workflow).

---

## 4. Como Executar

1.  No repositório do GitHub, vá em **Actions**.
2.  Selecione **Exercicio 1 AWS Pipeline**.
3.  Clique em **Run workflow**.
4.  Escolha o parâmetro:
    *   `deploy`: Para validar, testar e subir a stack.
    *   `delete`: Para limpar o ambiente e excluir a stack.

---

## Exemplo de Visualização (Console AWS)

### Identity Provider:
![IAM OIDC Provider](https://raw.githubusercontent.com/aws-actions/configure-aws-credentials/main/docs/assets/iam-identity-provider-details.png)

### Trust Relationship da Role:
![IAM Role Trust](https://raw.githubusercontent.com/aws-actions/configure-aws-credentials/main/docs/assets/iam-role-trust-relationship.png)
