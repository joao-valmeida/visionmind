# Guia de Deploy Azure - Exercício 1

Este guia explica como configurar a pipeline de CI/CD para o Exercício 1 no Azure, utilizando o Serverless Framework e GitHub Actions.

## 1. Configuração no Azure (App Registration)

Para que o GitHub consiga realizar o deploy, você precisa criar uma "Identidade" no Azure.

1.  **Criar Registro de Aplicativo**:
    *   Vá em **Entra ID (antigo Azure AD) > App Registrations > New Registration**.
    *   Nome: `github-actions-serverless`.
    *   Tipo de conta: `Accounts in this organizational directory only`.
2.  **Criar Segredo (Client Secret)**:
    *   Dentro do aplicativo criado, vá em **Certificates & secrets > Client secrets**.
    *   Clique em **+ New client secret**.
    *   **Importante**: Copie o **Value** do segredo imediatamente.
3.  **Atribuir Permissões (RBAC)**:
    *   Vá na sua **Subscription (Assinatura)** no Portal do Azure.
    *   Clique em **Access Control (IAM) > Add > Add role assignment**.
    *   **Role**: Selecione `Contributor` (Colaborador) na aba de *Privileged administrator roles*.
    *   **Members**: Selecione o aplicativo que você criou no passo 1.

## 2. Configuração no GitHub (Secrets)

No seu repositório GitHub, vá em **Settings > Secrets and variables > Actions** e adicione as seguintes secrets:

*   `AZURE_CLIENT_ID`: O "Application (client) ID" que aparece na visão geral do aplicativo no Azure.
*   `AZURE_TENANT_ID`: O "Directory (tenant) ID" do seu Azure.
*   `AZURE_SUBSCRIPTION_ID`: O ID da sua assinatura do Azure.
*   `AZURE_CLIENT_SECRET`: O valor do segredo que você criou no passo 1.2.

## 3. Detalhes Técnicos e Correções Realizadas

Durante a configuração, realizamos as seguintes correções para garantir a compatibilidade:

### Compatibilidade de Runtime (Python)
*   O plugin `serverless-azure-functions` (v2.x) possui limitações com o Python 3.9.
*   **Ajuste**: O runtime foi fixado em **Python 3.8** no arquivo `serverless.yml` e no workflow `.yml`.

### Autenticação do Plugin
*   O Serverless Framework no Azure pode tentar realizar um login interativo (Device Code).
*   **Ajuste**: Configuramos `authType: servicePrincipal` no `serverless.yml` para usar as credenciais automáticas das Secrets.

### Provedores de Recursos (Resource Providers)
*   Muitas assinaturas Azure vêm com recursos de monitoramento desabilitados por padrão.
*   **Ajuste**: Adicionamos um passo na pipeline para registrar os namespaces `microsoft.insights` e `microsoft.operationalinsights` via Azure CLI antes do deploy.

## 4. Como Executar

O deploy é disparado manualmente via GitHub Actions:
1. Vá na aba **Actions** do seu repositório.
2. Selecione o workflow **Exercicio 1 Azure Pipeline**.
3. Clique em **Run workflow**, escolha a ação (`deploy` ou `remove`) e execute.

---
*Nota: Se o deploy falhar na primeira execução por causa dos Resource Providers, aguarde 2 minutos e execute novamente (o registro no Azure leva um breve tempo para propagar).*
