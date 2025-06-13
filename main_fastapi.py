from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pipeline_gerar_leads import run_pipeline

app = FastAPI()

@app.post("/gerar-leads-completo")
def gerar_leads():
    try:
        run_pipeline()
        return JSONResponse(content={"status": "ok", "message": "Pipeline executado com sucesso."}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"status": "erro", "message": str(e)}, status_code=500)
