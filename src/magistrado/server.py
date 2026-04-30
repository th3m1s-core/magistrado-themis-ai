import json
from typing import Dict, Any

def generate_forensic_report(event_data: Dict[str, Any]) -> str:
    """
    Simula o motor de raciocínio jurídico do Magistrado Themis.
    """
    gtid = event_data.get("gtid", "UNKNOWN")
    score = event_data.get("score", 0)
    
    report = f"--- LAUDO FORENSE AUTOMATIZADO #{gtid[:8]} ---\n"
    report += f"Status: {'AUTÊNTICO' if score > 85 else 'SUSPEITO'}\n"
    report += f"Confiança: {score}%\n\n"
    report += "Análise: O sistema detectou padrões de microtextura consistentes com o registro original..."
    
    return report

if __name__ == "__main__":
    # Exemplo de uso
    sample_event = {"gtid": "0Z7F-4K2M", "score": 92.4}
    print(generate_forensic_report(sample_event))
