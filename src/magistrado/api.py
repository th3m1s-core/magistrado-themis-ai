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

@app.post("/v1/magistrado/laudo", response_model=Dict[str, str])
async def create_laudo(event: EventData):
    try:
        report = generate_forensic_report(event.dict())
        return {"laudo": report, "status": "ok"}
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
