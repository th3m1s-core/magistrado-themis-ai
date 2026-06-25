"""
Test script para o Magistrado Themis MCP Server.
Simula dois eventos: um AUTÊNTICO e um SUSPEITO.
"""
import sys
import os

# Add parent path
sys.path.insert(0, os.path.dirname(__file__))

from server import generate_forensic_report, run_security_check

print("=" * 80)
print("  TESTE 1: EVENTO SUSPEITO (score baixo, falha NFC)")
print("=" * 80)
report_suspeito = generate_forensic_report({
    "gtid": "GD-0Z7F-4K2M",
    "score": 61.2,
    "optical_similarity": 0.68,
    "rf_consistency": 0.0,
    "tamper_evidence": 1.0,
    "empresa": "FrotaTech Locações SA",
    "segmento": "frotista"
})
print(report_suspeito)

print("\n" + "=" * 80)
print("  TESTE 2: EVENTO AUTÊNTICO (score alto, todas métricas OK)")
print("=" * 80)
report_autentico = generate_forensic_report({
    "gtid": "GD-7A9F-2C4E",
    "score": 94.8,
    "optical_similarity": 0.97,
    "rf_consistency": 1.0,
    "tamper_evidence": 1.0,
    "empresa": "Seguradora Nacional de Frotas Ltda",
    "segmento": "seguradora"
})
print(report_autentico)

print("\n" + "=" * 80)
print("  TESTE 3: SECURITY CHECK — Ativo Integrado Externo")
print("=" * 80)
check = run_security_check({
    "app_domain": "https://api.frotapartner.com.br",
    "target_market": "finanças",
    "exposed_keys": ["private_key_nfc", "session_key_rfid"]
})
import json
print(json.dumps(check, indent=2, ensure_ascii=False))
