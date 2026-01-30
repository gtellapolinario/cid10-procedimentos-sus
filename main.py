from fastapi import FastAPI, HTTPException, Query

from typing import List, Optional
import json
import os

app = FastAPI(
    title="CID-10 API",
    description="Microserviço para consulta de códigos CID-10",
    version="1.0.0"
)

from fastapi.middleware.cors import CORSMiddleware

# --- Adiciona CORS (Permitir Frontend) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção: ["https://app.gtmedics.com", "http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Carregar dados em memória
CID_DB = []
SIGTAP_DB = []

@app.on_event("startup")
def load_db():
    global CID_DB, SIGTAP_DB
    
    # 1. Carregar CID-10
    try:
        # Tenta carregar do diretório dados/ se existir, senão tenta raiz (fallback)
        cid_path = "dados/cid10.json" if os.path.exists("dados/cid10.json") else "cid10.json"
        
        with open(cid_path, "r", encoding="utf-8") as f:
            CID_DB = json.load(f)
        print(f"✅ CID-10 carregado: {len(CID_DB)} registros.")
    except Exception as e:
        print(f"❌ Erro ao carregar CID-10: {e}")
        CID_DB = []

    # 2. Carregar Procedimentos (SIGTAP)
    try:
        proc_path = "dados/procedimentos.json"
        if os.path.exists(proc_path):
            with open(proc_path, "r", encoding="utf-8") as f:
                SIGTAP_DB = json.load(f)
            print(f"✅ SIGTAP carregado: {len(SIGTAP_DB)} registros.")
        else:
             print(f"⚠️ Arquivo de procedimentos não encontrado em {proc_path}")
    except Exception as e:
        print(f"❌ Erro ao carregar SIGTAP: {e}")
        SIGTAP_DB = []

@app.get("/")
def home():
    return {
        "status": "online", 
        "service": "Medical Tables API (CID + SIGTAP)", 
        "records": {
            "cid10": len(CID_DB),
            "sigtap": len(SIGTAP_DB)
        }
    }

# --- CID-10 ---

@app.get("/cid/search")
def search_cid(q: str = Query(..., min_length=3)):
    """Busca CID-10 por nome ou código"""
    query = q.lower().strip()
    results = [
        item for item in CID_DB 
        if query in item.get('description', '').lower() or query in item.get('code', '').lower()
    ]
    return {"count": len(results), "results": results[:50]}

@app.get("/cid/code/{codigo}")
def get_cid_by_code(codigo: str):
    """Busca exata CID-10 por código"""
    code = codigo.upper().strip()
    for item in CID_DB:
        if item.get('code') == code:
            return item
    raise HTTPException(404, "Código CID não encontrado")

# --- SIGTAP (Procedimentos) ---

@app.get("/sigtap/search")
def search_sigtap(q: str = Query(..., min_length=3)):
    """Busca Procedimento SIGTAP por nome ou código"""
    query = q.lower().strip()
    results = [
        item for item in SIGTAP_DB 
        if query in item.get('nome', '').lower() or query in item.get('codigo', '').lower()
    ]
    return {"count": len(results), "results": results[:50]}

@app.get("/sigtap/code/{codigo}")
def get_sigtap_by_code(codigo: str):
    """Busca exata SIGTAP por código"""
    code = codigo.strip()
    for item in SIGTAP_DB:
        if item.get('codigo') == code:
            return item
    raise HTTPException(404, "Código SIGTAP não encontrado")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
