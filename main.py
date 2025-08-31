from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
import os
import google.generativeai as genai
from dotenv import load_dotenv
import fitz
from fastapi.middleware.cors import CORSMiddleware
import json
from google.api_core import exceptions as google_exceptions

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

class Email(BaseModel):
  text: str

app = FastAPI()

origins = [
  "https://email-assistant.onrender.com",
  "http://localhost:5500",
  "http://127.0.0.1:5500",
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_methods=["*"],
  allow_headers=["*"],
)

def processLogic(text: str):
  if not text:
    raise HTTPException(status_code=400, detail="O campo de texto está vazio.")
  
  classification = classifyWithGemini(text)
  suggestion_obj = generateResponseWithGemini(text, classification)
  
  tasks = []
  if classification == "Produtivo":
    tasks_string = generateTasksWithGemini(text)
    if tasks_string and "não há tarefas" not in tasks_string.lower():
      tasks = [task.strip() for task in tasks_string.split(';')]
  
  return {
    "category": classification,
    "suggested_response": suggestion_obj,
    "tasks": tasks
  }
  

def classifyWithGemini(text: str):
  prompt = f"""
    Você é um assistente de triagem de e-mails altamente eficiente. Sua única tarefa é classificar o e-mail fornecido em uma de duas categorias: 'Produtivo' ou 'Improdutivo', com base em seu impacto no trabalho do destinatário.

    Regras de Classificação:
    - 'Produtivo': E-mails que contêm informações de negócio importantes ou que requerem uma ação. Inclui: faturas, relatórios, dúvidas de clientes, problemas técnicos, agendamentos, reclamações urgentes.
    - MUITO IMPORTANTE: E-mails informativos sobre tópicos de negócio cruciais (como confirmações de pagamento, atualizações de projeto, documentos legais) São 'Produtivos', mesmo que não exijam uma ação imediata. A informação em si é produtiva.
    - 'Improdutivo': E-mails que podem ser ignorados sem consequências diretas para o trabalho. Inclui: spam, newsletters, propaganda, notificações de redes sociais, e-mails informativos de baixa prioridade.

    O raciocínio é: se este e-mail fosse apagado e nunca lido, haveria algum impacto negativo? Se a resposta for sim, ele é 'Produtivo'.

    Analise o seguinte texto de e-mail e retorne APENAS a palavra 'Produtivo' ou 'Improdutivo'.

    E-mail:
    ---
    {text}
    ---
    Classificação:
  """

  try:
    response = model.generate_content(prompt)
    return response.text.strip()
  except google_exceptions.ResourceExhausted:
    raise HTTPException(status_code=429, detail="Limite diário de créditos da IA excedida. Tente novamente amanhã.")
  except Exception:
    raise HTTPException(status_code=500, detail="Erro ao comunicar com a IA.")


def generateResponseWithGemini(email_text: str, category: str):
  prompt = f"""
    Você é um assistente de e-mail. Sua tarefa é criar uma sugestão de resposta profissional para o e-mail fornecido.
    Retorne sua resposta como um objeto JSON com as seguintes chaves: "assunto", "conteudo".

    Categoria do E-mail: {category}
    Texto Original do E-mail:
    ---
    {email_text}
    ---

    Instruções:
    - Assunto: Crie um título de resposta apropriado, ex: "Re: [Assunto Original]".
    - Conteúdo: Escreva o corpo principal do e-mail. Se for produtivo, confirme a ação. Se a categoria for 'Improdutivo', sugira uma resposta muito curta e neutra para arquivamento.

    JSON de Resposta:
  """

  try:
    response = model.generate_content(prompt)
    json_response_text = response.text.strip().replace("```json", "").replace("```", "")
    return json.loads(json_response_text)
  except google_exceptions.ResourceExhausted:
    raise HTTPException(status_code=429, detail="Limite diário de créditos da IA excedida. Tente novamente amanhã.")
  except Exception:
    raise HTTPException(status_code=500, detail="Erro ao gerar sugestão de resposta.")


def generateTasksWithGemini(email_text: str):
  prompt = f"""
    Você é um assistente de produtividade. Sua tarefa é analisar o e-mail e extrair uma lista de ações ou tarefas claras para o destinatário.

    E-mail:
    ---
    {email_text}
    ---

    Instruções:
    - Liste apenas as tarefas para o destinatário.
    - Separe cada tarefa com um ponto e vírgula (;).
    - Se não houver nenhuma tarefa clara, retorne apenas a frase "Não há tarefas pendentes".
    - Você não precisa colocar o nome do responsável nas tarefas.

    Exemplo de retorno: "Revisar a proposta de orçamento; Enviar feedback até sexta-feira; Agendar reunião com o time de marketing"

    Tarefas:
  """

  try:
    response = model.generate_content(prompt)
    return response.text.strip()
  except google_exceptions.ResourceExhausted:
    raise HTTPException(status_code=429, detail="Limite diário de créditos da IA excedida. Tente novamente amanhã.")
  except Exception:
    raise HTTPException(status_code=500, detail="Erro ao gerar tarefas.")


@app.post('/processing-text')
async def processingText(email: Email):
  result = processLogic(email.text)
  result["source"] = "json_text"
  return result

@app.post('/processing-file')
async def processingFile(file: UploadFile = File(...)):
  extracted_text = ""

  if file.filename.endswith(".txt"):
    content_bytes = await file.read()
    extracted_text = content_bytes.decode("utf-8")
  elif file.filename.endswith(".pdf"):
    content_bytes = await file.read()
    with fitz.open(stream=content_bytes, filetype="pdf") as doc:
      for page in doc:
        extracted_text += page.get_text()
  else:
    raise HTTPException(status_code=400, detail="Formato de arquivo não suportado. Por favor, use .txt or .pdf.")
  
  result = processLogic(extracted_text)
  result["source"] = file.filename
  return result