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
    # Cenários adicionais para expandir dataset (GATE 1)
    {
        "gtid": "GD-1A2B-3C4D",
        "score": 15.0,
        "optical_similarity": 0.25,
        "rf_consistency": 0.0,
        "tamper_evidence": 0.10,
        "empresa": "Porto Seguro",
        "segmento": "seguradora",
        "_label": "fraude_sinistro_falsificado"
    },
    {
        "gtid": "GD-2E3F-4G5H",
        "score": 98.5,
        "optical_similarity": 0.99,
        "rf_consistency": 1.0,
        "tamper_evidence": 1.0,
        "empresa": "Localiza Rent a Car",
        "segmento": "locadora",
        "_label": "autentico_zero_km"
    },
    {
        "gtid": "GD-3I4J-5K6L",
        "score": 55.0,
        "optical_similarity": 0.60,
        "rf_consistency": 0.5,
        "tamper_evidence": 0.80,
        "empresa": "Movida",
        "segmento": "locadora",
        "_label": "suspeito_troca_placa"
    },
    {
        "gtid": "GD-4M5N-6O7P",
        "score": 82.0,
        "optical_similarity": 0.85,
        "rf_consistency": 1.0,
        "tamper_evidence": 0.95,
        "empresa": "JBS Logística",
        "segmento": "logistica",
        "_label": "autentico_carga_alta_valor"
    },
    {
        "gtid": "GD-5Q6R-7S8T",
        "score": 35.0,
        "optical_similarity": 0.40,
        "rf_consistency": 0.0,
        "tamper_evidence": 0.20,
        "empresa": "Allianz Seguros",
        "segmento": "seguradora",
        "_label": "critico_roubo_carga"
    },
    {
        "gtid": "GD-6U7V-8W9X",
        "score": 91.0,
        "optical_similarity": 0.93,
        "rf_consistency": 1.0,
        "tamper_evidence": 0.97,
        "empresa": "BRF Foods",
        "segmento": "logistica",
        "_label": "autentico_cadeia_frio"
    },
    {
        "gtid": "GD-7Y8Z-9A0B",
        "score": 67.0,
        "optical_similarity": 0.70,
        "rf_consistency": 0.8,
        "tamper_evidence": 0.85,
        "empresa": "Unidas",
        "segmento": "locadora",
        "_label": "suspeito_odor_combustivel"
    },
    {
        "gtid": "GD-8C1D-2E3F",
        "score": 45.0,
        "optical_similarity": 0.50,
        "rf_consistency": 0.3,
        "tamper_evidence": 0.40,
        "empresa": "Tokio Marine",
        "segmento": "seguradora",
        "_label": "suspeito_adesivo_reposicao"
    },
    {
        "gtid": "GD-9G4H-5I6J",
        "score": 96.0,
        "optical_similarity": 0.98,
        "rf_consistency": 1.0,
        "tamper_evidence": 1.0,
        "empresa": "Vale Logística",
        "segmento": "logistica",
        "_label": "autentico_minerio_ferro"
    },
    {
        "gtid": "GD-0K7L-8M9N",
        "score": 28.0,
        "optical_similarity": 0.35,
        "rf_consistency": 0.0,
        "tamper_evidence": 0.15,
        "empresa": "Mapfre",
        "segmento": "seguradora",
        "_label": "critico_impressao_3d"
    },
    {
        "gtid": "GD-1O5P-6Q7R",
        "score": 89.0,
        "optical_similarity": 0.92,
        "rf_consistency": 1.0,
        "tamper_evidence": 0.96,
        "empresa": "Ambev Logística",
        "segmento": "logistica",
        "_label": "autentico_bebidas_alcool"
    },
    {
        "gtid": "GD-2S8T-9U0V",
        "score": 72.0,
        "optical_similarity": 0.75,
        "rf_consistency": 0.9,
        "tamper_evidence": 0.78,
        "empresa": "Hertz",
        "segmento": "locadora",
        "_label": "suspeito_quilometragem_alterada"
    },
    {
        "gtid": "GD-3W9X-0Y1Z",
        "score": 52.0,
        "optical_similarity": 0.58,
        "rf_consistency": 0.4,
        "tamper_evidence": 0.60,
        "empresa": "Liberty Seguros",
        "segmento": "seguradora",
        "_label": "suspeito_chip_nfc_clonado"
    },
    {
        "gtid": "GD-4A0B-1C2D",
        "score": 95.0,
        "optical_similarity": 0.96,
        "rf_consistency": 1.0,
        "tamper_evidence": 0.99,
        "empresa": "Petrobras Distribuidora",
        "segmento": "logistica",
        "_label": "autentico_derivados_petroleo"
    },
    {
        "gtid": "GD-5E1F-2G3H",
        "score": 38.0,
        "optical_similarity": 0.42,
        "rf_consistency": 0.1,
        "tamper_evidence": 0.25,
        "empresa": "Zurich Seguros",
        "segmento": "seguradora",
        "_label": "critico_selo_quebrado"
    },
    {
        "gtid": "GD-6I2J-3K4L",
        "score": 87.0,
        "optical_similarity": 0.90,
        "rf_consistency": 1.0,
        "tamper_evidence": 0.94,
        "empresa": "Coca-Cola Brasil",
        "segmento": "logistica",
        "_label": "autentico_bebidas_nao_alcool"
    },
    {
        "gtid": "GD-7M3N-4O5P",
        "score": 63.0,
        "optical_similarity": 0.65,
        "rf_consistency": 0.7,
        "tamper_evidence": 0.75,
        "empresa": "Avis",
        "segmento": "locadora",
        "_label": "suspeito_ressonancia_magnetica"
    },
    {
        "gtid": "GD-8Q4R-5S6T",
        "score": 48.0,
        "optical_similarity": 0.52,
        "rf_consistency": 0.2,
        "tamper_evidence": 0.35,
        "empresa": "Suhai Seguros",
        "segmento": "seguradora",
        "_label": "suspeito_interferencia_jammer"
    },
    {
        "gtid": "GD-9U5V-6W7X",
        "score": 93.0,
        "optical_similarity": 0.95,
        "rf_consistency": 1.0,
        "tamper_evidence": 0.98,
        "empresa": "Carrefour Logística",
        "segmento": "varejo",
        "_label": "autentico_varejo_supermercado"
    },
    {
        "gtid": "GD-0Y6Z-7A8B",
        "score": 33.0,
        "optical_similarity": 0.38,
        "rf_consistency": 0.0,
        "tamper_evidence": 0.18,
        "empresa": "HD Seguros",
        "segmento": "seguradora",
        "_label": "critico_falsificacao_profissional"
    },
    {
        "gtid": "GD-1C7D-8E9F",
        "score": 90.0,
        "optical_similarity": 0.94,
        "rf_consistency": 1.0,
        "tamper_evidence": 0.97,
        "empresa": "Walmart Brasil",
        "segmento": "varejo",
        "_label": "autentico_varejo_atacado"
    },
    {
        "gtid": "GD-2G8H-9I0J",
        "score": 70.0,
        "optical_similarity": 0.73,
        "rf_consistency": 0.85,
        "tamper_evidence": 0.80,
        "empresa": "Budget",
        "segmento": "locadora",
        "_label": "suspeito_manipulacao_odbii"
    },
    {
        "gtid": "GD-3K9L-0M1N",
        "score": 58.0,
        "optical_similarity": 0.62,
        "rf_consistency": 0.5,
        "tamper_evidence": 0.65,
        "empresa": "Chubb Seguros",
        "segmento": "seguradora",
        "_label": "suspeito_anomalia_gps"
    },
    {
        "gtid": "GD-4O0P-1Q2R",
        "score": 97.0,
        "optical_similarity": 0.98,
        "rf_consistency": 1.0,
        "tamper_evidence": 1.0,
        "empresa": "Magazine Luiza Logística",
        "segmento": "e-commerce",
        "_label": "autentico_e_commerce"
    },
    {
        "gtid": "GD-5S1T-2U3V",
        "score": 41.0,
        "optical_similarity": 0.45,
        "rf_consistency": 0.0,
        "tamper_evidence": 0.22,
        "empresa": "AIG Brasil",
        "segmento": "seguradora",
        "_label": "critico_reproducao_fotografica"
    },
    {
        "gtid": "GD-6W2X-3Y4Z",
        "score": 86.0,
        "optical_similarity": 0.89,
        "rf_consistency": 1.0,
        "tamper_evidence": 0.93,
        "empresa": "Amazon Brasil",
        "segmento": "e-commerce",
        "_label": "autentico_logistica_ultimo_km"
    },
    {
        "gtid": "GD-7A3B-4C5D",
        "score": 65.0,
        "optical_similarity": 0.68,
        "rf_consistency": 0.75,
        "tamper_evidence": 0.72,
        "empresa": "National",
        "segmento": "locadora",
        "_label": "suspeito_interferencia_ir"
    },
    {
        "gtid": "GD-8E4F-5G6H",
        "score": 54.0,
        "optical_similarity": 0.57,
        "rf_consistency": 0.3,
        "tamper_evidence": 0.45,
        "empresa": "Generali",
        "segmento": "seguradora",
        "_label": "suspeito_ataque_replay"
    },
    {
        "gtid": "GD-9I5J-6K7L",
        "score": 92.0,
        "optical_similarity": 0.94,
        "rf_consistency": 1.0,
        "tamper_evidence": 0.96,
        "empresa": "Mercado Livre Logística",
        "segmento": "e-commerce",
        "_label": "autentico_marketplace"
    },
    {
        "gtid": "GD-0M6N-7O8P",
        "score": 36.0,
        "optical_similarity": 0.39,
        "rf_consistency": 0.0,
        "tamper_evidence": 0.16,
        "empresa": "Sompo Seguros",
        "segmento": "seguradora",
        "_label": "critico_adulteracao_chassi"
    },
    {
        "gtid": "GD-1Q7R-8S9T",
        "score": 88.0,
        "optical_similarity": 0.91,
        "rf_consistency": 1.0,
        "tamper_evidence": 0.95,
        "empresa": "RaiaDrogasil Logística",
        "segmento": "farmaceutico",
        "_label": "autentico_medicamentos"
    },
    {
        "gtid": "GD-2U8V-9W0X",
        "score": 69.0,
        "optical_similarity": 0.71,
        "rf_consistency": 0.8,
        "tamper_evidence": 0.77,
        "empresa": "Sixt",
        "segmento": "locadora",
        "_label": "suspeito_manipulacao_bluetooth"
    },
    {
        "gtid": "GD-3Y9X-0A1B",
        "score": 56.0,
        "optical_similarity": 0.60,
        "rf_consistency": 0.4,
        "tamper_evidence": 0.50,
        "empresa": "AXA Seguros",
        "segmento": "seguradora",
        "_label": "suspeito_injecao_dados"
    },
    {
        "gtid": "GD-4C0D-1E2F",
        "score": 94.0,
        "optical_similarity": 0.96,
        "rf_consistency": 1.0,
        "tamper_evidence": 0.98,
        "empresa": "Grupo Boticário",
        "segmento": "cosmeticos",
        "_label": "autentico_produtos_cosmeticos"
    },
    {
        "gtid": "GD-5G1H-2 I3J",
        "score": 44.0,
        "optical_similarity": 0.48,
        "rf_consistency": 0.1,
        "tamper_evidence": 0.28,
        "empresa": "HDI Seguros",
        "segmento": "seguradora",
        "_label": "suspeito_ataque_man_in_middle"
    },
    {
        "gtid": "GD-6K2L-3M4N",
        "score": 91.0,
        "optical_similarity": 0.93,
        "rf_consistency": 1.0,
        "tamper_evidence": 0.97,
        "empresa": "Natura Logística",
        "segmento": "cosmeticos",
        "_label": "autentico_produtos_naturais"
    },
    {
        "gtid": "GD-7O3P-4Q5R",
        "score": 62.0,
        "optical_similarity": 0.64,
        "rf_consistency": 0.6,
        "tamper_evidence": 0.68,
        "empresa": "Europcar",
        "segmento": "locadora",
        "_label": "suspeito_interferencia_ble"
    },
    {
        "gtid": "GD-8S4T-5U6V",
        "score": 50.0,
        "optical_similarity": 0.53,
        "rf_consistency": 0.2,
        "tamper_evidence": 0.38,
        "empresa": "Porto Seguro Saúde",
        "segmento": "saude",
        "_label": "suspeito_falsificacao_equipamento"
    },
    {
        "gtid": "GD-9W5X-6Y7Z",
        "score": 96.0,
        "optical_similarity": 0.97,
        "rf_consistency": 1.0,
        "tamper_evidence": 0.99,
        "empresa": "Hospital Albert Einstein",
        "segmento": "saude",
        "_label": "autentico_equipamentos_medicos"
    },
    {
        "gtid": "GD-0A6B-7C8D",
        "score": 39.0,
        "optical_similarity": 0.41,
        "rf_consistency": 0.0,
        "tamper_evidence": 0.19,
        "empresa": "Bradesco Seguros",
        "segmento": "seguradora",
        "_label": "critico_selo_substituido"
    },
    {
        "gtid": "GD-1E7F-8G9H",
        "score": 89.0,
        "optical_similarity": 0.92,
        "rf_consistency": 1.0,
        "tamper_evidence": 0.96,
        "empresa": "Fleury Medicina",
        "segmento": "saude",
        "_label": "autentico_amostras_biologicas"
    },
    {
        "gtid": "GD-2I8J-9K0L",
        "score": 66.0,
        "optical_similarity": 0.69,
        "rf_consistency": 0.7,
        "tamper_evidence": 0.74,
        "empresa": "Goldcar",
        "segmento": "locadora",
        "_label": "suspeito_anomalia_tempo_real"
    },
    {
        "gtid": "GD-3M9N-0O1P",
        "score": 52.0,
        "optical_similarity": 0.55,
        "rf_consistency": 0.3,
        "tamper_evidence": 0.42,
        "empresa": "Itaú Seguros",
        "segmento": "seguradora",
        "_label": "suspeito_correlacao_anomala"
    },
    {
        "gtid": "GD-4Q0P-1R2S",
        "score": 93.0,
        "optical_similarity": 0.95,
        "rf_consistency": 1.0,
        "tamper_evidence": 0.98,
        "empresa": "Sabin Laboratórios",
        "segmento": "saude",
        "_label": "autentico_resultados_exames"
    },
    {
        "gtid": "GD-5T1U-2V3W",
        "score": 47.0,
        "optical_similarity": 0.50,
        "rf_consistency": 0.15,
        "tamper_evidence": 0.32,
        "empresa": "Santander Seguros",
        "segmento": "seguradora",
        "_label": "suspeito_padrao_sintetico"
    },
    {
        "gtid": "GD-6X2Y-3Z4A",
        "score": 95.0,
        "optical_similarity": 0.96,
        "rf_consistency": 1.0,
        "tamper_evidence": 0.99,
        "empresa": "Dasa Diagnósticos",
        "segmento": "saude",
        "_label": "autentico_imagens_medicas"
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
