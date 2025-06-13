from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pipeline_gerar_leads import run_pipeline

# --- Modelo de entrada para validar o que a API recebe ---
class SearchInput(BaseModel):
    term: str
    pages: int = 1 # O número de páginas do DuckDuckGo a serem pesquisadas

app = FastAPI(
    title="API de Geração de Leads",
    description="Busca um termo no DuckDuckGo, visita os sites e extrai informações de contato."
)

@app.post("/gerar-leads-completo")
def gerar_leads(search_input: SearchInput):
    """
    Versão de TESTE (Smoke Test) para verificar se a API responde.
    Esta versão NÃO executa o pipeline de scraping.
    """
    # --- INÍCIO DO CÓDIGO DE TESTE ---

    print("--- ENDPOINT DE TESTE FOI ATINGIDO COM SUCESSO ---")
    print(f"Termo recebido do n8n: {search_input.term}")
    print(f"Páginas recebidas do n8n: {search_input.pages}")

    # A chamada para o pipeline pesado (run_pipeline) está desativada para este teste.
    # Ao reativá-la, lembre-se de colocar o bloco de código dentro de um try...except.
    
    # Retorna uma resposta imediata para provar que a API está viva.
    return {
        "status": "sucesso - TESTE DE FUMAÇA OK",
        "message": "A API está respondendo corretamente. O problema ocorre dentro do pipeline de scraping.",
        "dados_recebidos": {
            "termo": search_input.term,
            "paginas": search_input.pages
        }
    }
    # --- FIM DO CÓDIGO DE TESTE ---