# Configuração do Firebase para o Sistema SUMESE

Para que o sistema funcione corretamente, você precisa configurar o Firebase e adicionar as credenciais ao Streamlit.

## 1. Criar Projeto no Firebase
1. Acesse o [Console do Firebase](https://console.firebase.google.com/).
2. Clique em **"Adicionar projeto"** e dê um nome (ex: `sumese-app`).
3. Siga as instruções para criar o projeto.

## 2. Configurar o Authentication
1. No menu lateral, clique em **Criação** > **Authentication**.
2. Clique em **"Vamos começar"**.
3. Na aba **Sign-in method**, ative o provedor **Email/Senha**.
4. Vá na aba **Users** e crie um usuário para teste (ex: `admin@sumese.jus.br` com uma senha).

## 3. Configurar o Firestore (Banco de Dados)
1. No menu lateral, clique em **Criação** > **Firestore Database**.
2. Clique em **"Criar banco de dados"**.
3. Escolha um local para o servidor (ex: `nam5` ou `sa-east1` se disponível).
4. Escolha iniciar no **modo de produção** ou **modo de teste** (para desenvolvimento rápido, modo de teste libera acesso temporário, mas para este app, usaremos credenciais de serviço que têm acesso total, então as regras de segurança podem ser restritivas para acesso público).

## 4. Obter a Chave de Serviço (Service Account)
Esta chave permite que o Streamlit acesse o banco de dados como administrador.
1. No console do Firebase, clique na engrenagem ⚙️ ao lado de "Visão geral do projeto" > **Configurações do projeto**.
2. Vá na aba **Contas de serviço**.
3. Clique em **"Gerar nova chave privada"**.
4. Um arquivo `.json` será baixado. **Não compartilhe este arquivo**.

## 5. Obter a Web API Key (Para Login)
Esta chave é necessária para fazer login com email/senha.
1. Ainda em **Configurações do projeto**, vá na aba **Geral**.
2. Role até "Seus aplicativos" e, se não houver um App Web, clique no ícone `</>` (Web) para criar um.
3. Dê um nome ao app.
4. Após criar, você verá um campo `apiKey` no código de configuração exibido. Copie este valor.

## 6. Configurar o `secrets.toml` no Streamlit
O Streamlit usa um arquivo de segredos para guardar chaves privadas.

**Localmente:** Crie uma pasta `.streamlit` na raiz do projeto e dentro dela um arquivo `secrets.toml`.

**No Streamlit Cloud:** Nas configurações do app, vá em "Secrets".

O conteúdo do arquivo `secrets.toml` deve seguir este formato (substitua os valores):

```toml
[firebase_web]
api_key = "COLE_SUA_API_KEY_AQUI"

[firebase]
type = "service_account"
project_id = "seu-project-id"
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n..."
client_email = "..."
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."
```

> **Dica:** Abra o arquivo JSON baixado no passo 4 e copie o conteúdo de cada campo para a seção `[firebase]` do toml.

## 7. Rodar o App
No terminal, execute:
```bash
streamlit run app.py
```
