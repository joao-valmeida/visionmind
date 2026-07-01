# **Product Requirements Document (PRD)**

**Produto:** VisionMind Analyzer

**Data:** 30 de Junho de 2026

**Status:** Aprovado / Em Implementação

## **Sumário**

* [1\. Visão Geral e Objetivo do Produto](#bookmark=id.he6oya99jy4e)  
* [2\. Público-Alvo e Personas](#bookmark=id.fnfeet6yyozi)  
* [3\. Escopo e Requisitos Funcionais](#bookmark=id.9d8qalh8wj8g)  
* [4\. Arquitetura e Decisões Técnicas](#bookmark=id.satjl1e4b70d)  
* [5\. Requisitos Não Funcionais (NFRs)](#bookmark=id.vza5igv3ji3r)  
  * [5.1. Segurança e Conformidade (Princípios OWASP e IAM)](#bookmark=id.9ueezutr0olw)  
  * [5.2. Escalabilidade e Performance](#bookmark=id.hv1mhcqyn7wg)  
  * [5.3. FinOps e Estimativa de Custo (TCO)](#bookmark=id.lv6xpbmfu95v)  
* [6\. Estratégia de CI/CD e Qualidade (DevSecOps)](#bookmark=id.kz8c301aqjaf)  
* [7\. Métricas de Sucesso e KPIs](#bookmark=id.1a2ybrwdmu79)  
* [8\. Fora de Escopo (Out of Scope)](#bookmark=id.q9boswlb9p6v)

## **1\. Visão Geral e Objetivo do Produto**

A **VisionMind** é uma startup de IA voltada para o mercado corporativo de mídia. O produto em desenvolvimento consiste em um pipeline serverless altamente escalável que extrai, de forma automatizada, metadados, tags descritivas e nível de confiança de imagens assim que são armazenadas na nuvem.

**Objetivo de Negócio:** Eliminar o processo manual de catalogação de acervos fotográficos, acelerando a indexação e a busca em bancos de imagens através de Inteligência Artificial nativa em nuvem, garantindo um modelo de custos sustentável (Pay-as-you-go).

## **2\. Público-Alvo e Personas**

* **Editor de Fotografia:** Profissional que gerencia grandes volumes de imagens e precisa de automação para categorizá-las e torná-las pesquisáveis rapidamente.  
* **Sistemas Parceiros (B2B):** Aplicações de terceiros que enviarão imagens via API/SDK para a nossa infraestrutura e consumirão as tags do banco de dados para suas próprias lógicas de negócio.

## **3\. Escopo e Requisitos Funcionais**

### **User Stories Principais**

* **US01:** Como um Sistema Parceiro, quero fazer upload de uma imagem (JPEG/PNG) para um bucket do S3 para que o processamento seja iniciado automaticamente.  
* **US02:** Como um Sistema de Busca, quero consultar as tags extraídas e a confiabilidade gerada pela IA, para que eu possa exibir imagens relevantes na pesquisa.

### **Fluxo de Ponta a Ponta (Happy Path)**

1. **Ingestão:** O usuário/sistema faz o upload de uma imagem (PNG/JPG) no *Object Storage*.  
2. **Gatilho (Trigger):** O Storage detecta a criação do objeto e dispara um evento.  
3. **Computação:** Uma função serverless é invocada, validando o tipo de arquivo.  
4. **IA:** A função consome um serviço de AI Vision, que retorna um array de tags e percentuais de confiança.  
5. **Persistência:** A função consolida o *payload* e grava o metadado em um banco NoSQL para posterior consumo.

## **4\. Arquitetura e Decisões Técnicas**

O sistema adota uma **Arquitetura Orientada a Eventos (Event-Driven)** e **Serverless**, provisionada através de **Infraestrutura como Código (Terraform)**.

### **Topologia AWS (Stack Escolhida)**

A escolha da Amazon Web Services (AWS) baseia-se na forte integração nativa entre armazenamento, computação e inteligência artificial, minimizando custos de tráfego de rede e o tempo de desenvolvimento.

* **Storage:** Amazon S3 (Bucket).  
* **Computação:** AWS Lambda (Python 3.10).  
* **IA Vision:** Amazon Rekognition (DetectLabels).  
* **Banco de Dados:** Amazon DynamoDB (NoSQL).

### **Diagrama Arquitetural**

*(Abaixo, a representação em Mermaid da arquitetura. Suportada nativamente no GitLab/GitHub)*

graph TD  
    User\[Usuário / Cliente HTTP\] \--\>|Upload| S3\[Amazon S3 \\n Bucket: visionmind-raw-images\]  
    S3 \-- Trigger: s3:ObjectCreated \--\> Lambda\[AWS Lambda \\n Função Python\]  
    IAM{{IAM Role: \\n Least Privilege}} \-.-\>|Permissões| Lambda  
    Lambda \--\>|API Boto3| Rekognition\[Amazon Rekognition\]  
    Rekognition \--\>|Retorna Tags| Lambda  
    Lambda \--\>|API Boto3| DynamoDB\[(Amazon DynamoDB \\n Tabela: ImageMetadata)\]

## **5\. Requisitos Não Funcionais (NFRs)**

### **5.1. Segurança e Conformidade (Princípios OWASP e IAM)**

* **Validação de Input (OWASP):** O código Python (Lambda) aplica uma política estrita de *Allowlist* nas extensões de arquivo (.jpg, .jpeg, .png), bloqueando tentativas de injeção de arquivos maliciosos.  
* **IAM Least Privilege:** O perfil de execução do Lambda (configurado no Terraform) possui políticas (Policies) granulares restritas ao ARN (Amazon Resource Name) específico do bucket S3 e da tabela do DynamoDB. Não são permitidas permissões globais (\* em recursos, exceto Rekognition onde é mandatório pela AWS).  
* **Gestão de Segredos:** Ausência de chaves de API ou credenciais de banco de dados *hardcoded* no código-fonte. O acesso é governado via *AssumeRole* nativo do IAM.

### **5.2. Escalabilidade e Performance**

* O sistema opera com paradigma **Scale-to-Zero**, não consumindo capacidade ociosa quando não há uploads.  
* **Cold Start:** O código Python inicializa os clientes Boto3 fora do *handler* para reaproveitamento de conexões TCP, otimizando invocações subsequentes.

### **5.3. FinOps e Estimativa de Custo (TCO)**

As configurações (como o DynamoDB em modo *Pay-Per-Request* e o limite de tags MaxLabels=10 no Rekognition) visam otimizar custos.

**Estimativa Mensal (Cenário de 10.000 imagens/mês, 2MB média):**

* **S3:** \~$0.46  
* **Lambda:** $0.00 (Free Tier)  
* **DynamoDB:** $0.00 (Free Tier)  
* **Rekognition:** $10.00 ($1.00 por mil imagens)  
* **Total Estimado:** **\~$10.46 / mês**

## **6\. Estratégia de CI/CD e Qualidade (DevSecOps)**

O projeto adota uma esteira de *Continuous Integration / Continuous Deployment* gerenciada via **Jenkins**, utilizando *runners* hospedadas em infraestrutura Windows nativa.

* **SAST (Static Application Security Testing):** Varredura no código Python utilizando **Semgrep** para detectar injeções e falhas lógicas antes da compilação.  
* **SCA (Software Composition Analysis):** Geração de SBOM via **cdxgen** integrado ao *Dependency Track* para validar vulnerabilidades em bibliotecas de terceiros.  
* **Automação (IaC):** O processo de deploy compacta a aplicação nativamente (Compress-Archive) e aplica as mudanças de infraestrutura utilizando o binário do **Terraform**. As credenciais de deploy da nuvem ficam armazenadas como segredos no Jenkins e são expostas temporariamente durante a pipeline.

## **7\. Métricas de Sucesso e KPIs**

1. **Performance:** Tempo médio de processamento total (Upload até DynamoDB) inferiror a 3 segundos.  
2. **Segurança:** 0 (zero) vulnerabilidades Críticas ou Altas reportadas pelos scans SAST/SCA durante a etapa de *build*.  
3. **Disponibilidade:** Taxa de sucesso de processamento \> 99.9%.

## **8\. Fora de Escopo (Out of Scope)**

Nesta fase, **NÃO** faz parte da entrega:

* Frontend (Interface gráfica do usuário para consulta e upload manual).  
* Processamento e marcação de vídeos (Apenas imagens estáticas suportadas).  
* Configuração de infraestrutura Cloud *Multi-Region* (Disaster Recovery Avançado).