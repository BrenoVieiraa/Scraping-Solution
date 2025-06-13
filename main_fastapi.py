from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pipeline_gerar_leads import run_pipeline

# --- NOVO: Modelo de entrada para validar o que a API recebe ---
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
    Recebe um termo de busca e retorna uma lista de leads encontrados.
    """
    print(f"Iniciando pipeline para o termo: '{search_input.term}'")
    try:
        # --- MUDANÇA: Passa o input para o pipeline e recebe os resultados ---
        leads_encontrados = run_pipeline(
            text_to_find=search_input.term, 
            pages=search_input.pages
        )
        
        if not leads_encontrados:
            return {"status": "sucesso", "message": "Nenhum lead encontrado.", "data": []}
            
        return {"status": "sucesso", "data": leads_encontrados}

    except Exception as e:
        # Se algo der errado no pipeline, levanta uma exceção HTTP
        print(f"Erro no pipeline: {e}")
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro interno: {str(e)}")