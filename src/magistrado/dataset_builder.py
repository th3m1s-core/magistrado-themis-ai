# -*- coding: utf-8 -*-
"""
Magistrado Themis — Dataset Builder v0.1
Ferramenta para criar pares de treino {evento_json} -> {laudo_forense}
"""
import json
import os
from datetime import datetime

DATASET_PATH = "dataset/forensic_dataset.jsonl"

def create_entry(gtid, score, optical_sim, rf_status, tamper_status, laudo_texto):
    """Cria uma entrada formatada para o dataset."""
    entry = {
        "input": {
            "gtid": gtid,
            "metrics": {
                "trust_score": score,
                "optical_similarity": optical_sim,
                "rf_consistency": rf_status,
                "tamper_evidence": tamper_status
            },
            "timestamp": datetime.utcnow().isoformat()
        },
        "output": laudo_texto
    }
    return entry

def save_entry(entry):
    """Salva a entrada no arquivo .jsonl."""
    os.makedirs(os.path.dirname(DATASET_PATH), exist_ok=True)
    with open(DATASET_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"[Dataset] Entrada salva para o GTID: {entry['input']['gtid']}")

if __name__ == "__main__":
    # Exemplo de criação manual (Active Learning Loop)
    print("--- Magistrado Themis: Dataset Builder ---")
    
    # Simulação de um evento suspeito
    suspeito = create_entry(
        gtid="0Z7F-4K2M",
        score=61.2,
        optical_sim=0.68,
        rf_status=0, # Falha no NFC
        tamper_status=1.0, # Integridade física OK
        laudo_texto=(
            "Laudo de Autenticidade #0042 — SUSPEITO. Análise óptica indica "
            "divergência de 32% no padrão de microtextura. Ausência de sinal RF "
            "(esperado: NFC ativo) indica possível reprodução por impressão. "
            "Recomenda-se inspeção física imediata. Confiança: 61.2/100."
        )
    )
    
    save_entry(suspeito)
