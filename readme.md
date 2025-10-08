# Assistente Inteligente de E-mails

Python | FastAPI | HTML | JavaScript | Render

---

### [Acessar a Aplicação Online](https://email-assistant-frontend-nez0.onrender.com/)

## Descrição

O **E-mail Assistant** é uma aplicação full-stack projetada para otimizar a gestão de e-mails através de Inteligência Artificial. A ferramenta analisa o conteúdo de um e-mail (enviado via texto, ou por arquivos .txt ou .pdf), classifica como `produtivo` ou `improdutivo`, gera uma lista de tarefas e sugere uma resposta completa, economizando tempo e aumentando a produtividade do usuário.

## Funcionalidades Principais

* **Análise Multi-formato:** Aceita entrada de texto diretamente na textarea, ou por upload de arquivos `.txt` e `.pdf`.
* **Classificação Inteligente:** Utiliza a API do Google Gemini para classificar e-mails como **Produtivo** (requer ação/atenção) ou **Improdutivo** (spam, newsletters, etc).
* **Sugestão de Resposta Estruturada:** Gera uma sugestão de resposta completa, separada em `Assunto` e `Conteúdo`.
* **Lista de Tarefas:** Identifica e lista as tarefas e ações que o destinatário precisa executar com base no conteúdo do e-mail.
* **Responsividade:** O frontend foi desenvolvido para funcionar em desktops e também dispositivos móveis.

## Tecnologias Utilizadas

* **Backend:**
  * **Linguagem:** Python 3
  * **Framework:** FastAPI
  * **Inteligência Artificial:** Google Gemini API (`gemini-1.5-flash`)
  * **Servidor:** Uvicorn
* **Frontend:**
  * HTML
  * CSS
  * JavaScript
* **Deploy:**
  * **Plataforma:** Render

## Como Executar Localmente

Para rodar este projeto localmente, siga os passos abaixo:

1.  **Clone o repositório:**
  ```bash
  git clone [https://github.com/natanloc/email-assistant](https://github.com/natanloc/email-assistant)
  cd email-assistant
  ```

2.  **Crie e ative o ambiente virtual:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

3.  **Instale as dependências do backend:**
  ```bash
  pip install -r requirements.txt
  ```

4.  **Configure a chave da API:**
  * **Obtendo a Chave da API do Google Gemini:**

    1.  Acesse o **Google AI Studio**: [makersuite.google.com](https://makersuite.google.com).
    2.  Faça login com a conta do Google.
    3.  No menu à esquerda, clique em **"Get API key"**.
    4.  Clique em **"Create API key in new project"**.
    5.  Copie a chave gerada.

  * **Adicionando a Chave ao Projeto:**

    1.  Crie um arquivo chamado `.env` na raiz do projeto.
    2.  Dentro dele, adicione a seguinte linha, substituindo "SUA_CHAVE_SECRETA_DO_GEMINI" pelo valor da sua chave gerada:
      ```
      GEMINI_API_KEY="SUA_CHAVE_SECRETA_DO_GEMINI"
      ```

5.  **Inicie o servidor backend:**
  ```bash
  uvicorn main:app --reload
  ```
  O backend estará rodando em `http://127.0.0.1:8000`.

6.  **Abra o frontend:**
  * Navegue até a pasta `front`.
  * Rode o arquivo `index.html` na porta :5500 (é recomendado usar a extensão "Live Server" do VS Code).

7.  **Limitações do protótipo:**
  * Esse projeto usa a API gratuita do Gemini, portanto possui uma limitação diária de requisições que, ao ser excedida, exibe um erro para o usuário avisando que o limite de créditos da IA foi excedido.
  * Ao evoluir o projeto para ser publicado oficialmente, faríamos o upgrade da API para que não houvesse essa limitação.
