import re
import json
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

try:
    from server import generate_forensic_report, run_security_check
except ImportError:
    from magistrado.server import generate_forensic_report, run_security_check

app = FastAPI(
    title="Magistrado Themis API", 
    version="0.2.0",
    description="Motor de inteligência artificial forense para geração de laudos técnicos-jurídicos e auditoria de ativos do ecossistema Symbeon/GuardDrive"
)

class EventData(BaseModel):
    gtid: str
    score: float
    optical_similarity: float
    rf_consistency: float
    tamper_evidence: float
    empresa: str
    segmento: str

class SecurityCheckData(BaseModel):
    app_domain: str
    target_market: str
    exposed_keys: Optional[List[str]] = []

@app.post("/v1/magistrado/laudo", response_model=Dict[str, Any])
async def create_laudo(event: EventData):
    try:
        report = generate_forensic_report(event.dict())
        
        # Extrai metadados criptográficos reais do laudo gerado
        sig_match = re.search(r"Assinatura Digital Ed25519:\s+([a-f0-9]+)", report)
        pub_match = re.search(r"Chave Pública de Validação:\s+([a-f0-9]+)", report)
        block_match = re.search(r"Protocolado sob o Bloco L2:\s+(\d+)", report)
        
        signature = sig_match.group(1) if sig_match else "N/A"
        public_key = pub_match.group(1) if pub_match else "N/A"
        block_num = int(block_match.group(1)) if block_match else None
        
        return {
            "laudo": report,
            "status": "ok",
            "signature": signature,
            "public_key": public_key,
            "block_num": block_num
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/magistrado/security_check", response_model=Dict[str, Any])
async def security_check(data: SecurityCheckData):
    try:
        result = run_security_check(data.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
