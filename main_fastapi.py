from fastapi import FastAPI
from pydantic import BaseModel

# Definindo o modelo de entrada aqui mesmo para não importar nada
class SearchInput(BaseModel):
    term: str
    pages: int = 1

app = FastAPI(title="API de Teste Definitivo")

@app.get("/")
def read_root():
    """Endpoint raiz para um teste GET simples."""
    print("--- ENDPOINT RAIZ (GET) ATINGIDO ---")
    return {"Hello": "World", "Status": "API base está no ar"}

@app.post("/gerar-leads-completo")
def gerar_leads_teste(search_input: SearchInput):
    """Endpoint de teste POST que não faz nada além de responder."""
    print("--- ENDPOINT TESTE (POST) ATINGIDO ---")
    return {
        "status": "sucesso - TESTE DEFINITIVO OK",
        "message": "A API responde a POSTs. O problema não está na base.",
        "dados_recebidos": search_input.dict()
    }