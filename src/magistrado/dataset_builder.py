# -*- coding: utf-8 -*-
"""
Magistrado Themis — Dataset Builder v0.2
Active Learning Loop: cria pares de treino {evento_json} -> {laudo_forense}

Uso: python dataset_builder.py [--batch] [--output PATH]
"""
import json
import os
import sys
import argparse
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Importa o motor de geração de laudos
try:
    from server import generate_forensic_report
except ImportError:
    from magistrado.server import generate_forensic_report

DEFAULT_DATASET_PATH = "dataset/forensic_dataset.jsonl"


# ── Exemplos de seed para o Active Learning ────────────────────────────────
SEED_EVENTS = [
    {
        "gtid": "GD-0Z7F-4K2M",
        "score": 61.2,
        "optical_similarity": 0.68,
        "rf_consistency": 0.0,
        "tamper_evidence": 1.0,
        "empresa": "FrotaTech Locações SA",
        "segmento": "frotista",
        "_label": "suspeito_clonagem_optica"
    },
    {
        "gtid": "GD-7A9F-2C4E",
        "score": 94.8,
        "optical_similarity": 0.97,
        "rf_consistency": 1.0,
        "tamper_evidence": 1.0,
        "empresa": "Seguradora Nacional de Frotas Ltda",
        "segmento": "seguradora",
        "_label": "autentico_todos_conformes"
    },
    {
        "gtid": "GD-3X1B-9E7F",
        "score": 42.0,
        "optical_similarity": 0.55,
        "rf_consistency": 0.0,
        "tamper_evidence": 0.30,
        "empresa": "Pátio Nacional Remarcados",
        "segmento": "outro",
        "_label": "critico_adulteracao_fisica"
    },
    {
        "gtid": "GD-5C2D-8A1E",
        "score": 88.3,
        "optical_similarity": 0.91,
        "rf_consistency": 1.0,
        "tamper_evidence": 0.98,
        "empresa": "FrotaMinas Logística",
        "segmento": "frotista",
        "_label": "autentico_leve_desgaste"
    },
    {
        "gtid": "GD-9F4A-3B7C",
        "score": 73.5,
        "optical_similarity": 0.79,
        "rf_consistency": 1.0,
        "tamper_evidence": 0.72,
        "empresa": "Aliança Seguros Corporativos",
        "segmento": "seguradora",
        "_label": "suspeito_violacao_parcial"
    },
]


def save_entry(entry: dict, path: str = DEFAULT_DATASET_PATH):
    """Salva um par de treinamento no dataset JSONL."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"[Dataset] ✅ Entrada salva · GTID: {entry['input']['gtid']} · Label: {entry.get('_label', 'sem_label')}")


def build_entry_from_event(event: dict, laudo: str) -> dict:
    """Monta o par {input, output} para o dataset de fine-tuning."""
    label = event.pop("_label", "manual")
    return {
        "_label": label,
        "input": {
            "gtid": event["gtid"],
            "metrics": {
                "trust_score": event["score"],
                "optical_similarity": event["optical_similarity"],
                "rf_consistency": event["rf_consistency"],
                "tamper_evidence": event["tamper_evidence"]
            },
            "empresa": event.get("empresa", ""),
            "segmento": event.get("segmento", ""),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        },
        "output": laudo
    }


def run_batch(output_path: str = DEFAULT_DATASET_PATH):
    """Processa todos os eventos seed e salva os laudos no dataset."""
    print(f"\n🧠 Magistrado Themis — Active Learning Loop")
    print(f"📁 Destino: {output_path}")
    print(f"⚙️  Processando {len(SEED_EVENTS)} eventos seed...\n")

    for event in SEED_EVENTS:
        event_copy = dict(event)  # não mutilamos o original
        laudo = generate_forensic_report(event_copy)
        # Evita gravar a entrada automática dupla do server.py
        entry = build_entry_from_event(dict(event), laudo)
        save_entry(entry, output_path)

    print(f"\n✅ Batch concluído. {len(SEED_EVENTS)} laudos gerados e salvos.")


def run_interactive(output_path: str = DEFAULT_DATASET_PATH):
    """CLI interativa para criar entradas manualmente (Active Learning)."""
    print("\n🏛️  Magistrado Themis — Modo Interativo")
    print("   Crie pares de treino para fine-tuning do modelo.\n")

    while True:
        print("-" * 60)
        gtid = input("GTID do veículo (ou 'q' para sair): ").strip()
        if gtid.lower() == "q":
            break

        try:
            score = float(input("Score de confiança (0–100): "))
            optical_similarity = float(input("Similitude óptica (0.0–1.0): "))
            rf_consistency = float(input("Consistência RF (0.0 ou 1.0): "))
            tamper_evidence = float(input("Integridade do selo (0.0–1.0): "))
            empresa = input("Empresa solicitante: ").strip()
            segmento = input("Segmento (frotista/seguradora/outro): ").strip()
            label = input("Rótulo para o dataset (ex: suspeito_clonagem): ").strip()
        except ValueError as e:
            print(f"[ERRO] Valor inválido: {e}")
            continue

        event = {
            "gtid": gtid,
            "score": score,
            "optical_similarity": optical_similarity,
            "rf_consistency": rf_consistency,
            "tamper_evidence": tamper_evidence,
            "empresa": empresa,
            "segmento": segmento,
        }

        print("\n[...] Gerando laudo automatizado...\n")
        laudo = generate_forensic_report(event)
        print(laudo)

        confirma = input("\n✅ Salvar este laudo no dataset? (s/n): ").strip().lower()
        if confirma == "s":
            entry = {
                "_label": label or "manual",
                "input": {
                    "gtid": gtid,
                    "metrics": {
                        "trust_score": score,
                        "optical_similarity": optical_similarity,
                        "rf_consistency": rf_consistency,
                        "tamper_evidence": tamper_evidence
                    },
                    "empresa": empresa,
                    "segmento": segmento,
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                },
                "output": laudo
            }
            save_entry(entry, output_path)
        else:
            print("[Dataset] Entrada descartada.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Magistrado Themis — Dataset Builder")
    parser.add_argument("--batch", action="store_true", help="Processa eventos seed automaticamente")
    parser.add_argument("--output", type=str, default=DEFAULT_DATASET_PATH, help="Caminho do arquivo .jsonl de saída")
    args = parser.parse_args()

    if args.batch:
        run_batch(args.output)
    else:
        run_interactive(args.output)
