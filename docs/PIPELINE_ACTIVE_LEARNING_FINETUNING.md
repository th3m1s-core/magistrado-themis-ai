# 🧠 Magistrado Themis — Active Learning Loop & Fine-Tuning Pipeline
## Guia Técnico Completo dos Gates 1 e 2

> **Classificação:** Técnico | Symbeon Labs
> **Data:** 2026-06-30

---

## Visão Geral do Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│  GATE 1 — Active Learning Loop                                       │
│                                                                      │
│  SEED_EVENTS (18 cenários)                                           │
│      │                                                               │
│      ▼ [1B] run_batch()                                              │
│  for event in SEED_EVENTS:                                           │
│      │ [1C] generate_forensic_report(event)  ← server.py            │
│      │ [1D] build_entry_from_event()                                 │
│      │ [1E] save_entry() → forensic_dataset.jsonl                    │
│      ▼                                                               │
│  dataset/forensic_dataset.jsonl  (125+ entradas, 533KB)              │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│  GATE 2 — Fine-Tuning QLoRA                                          │
│                                                                      │
│  [2A] load_dataset(path)     → Dataset HuggingFace                  │
│  [2B] BitsAndBytesConfig     → 4-bit quantização NF4                │
│  [2C] AutoModelForCausalLM   → Qwen/Qwen2.5-3B-Instruct            │
│  [2D] prepare_model_for_kbit_training()                              │
│  [2E] get_peft_model()       → LoRA r=16, alpha=32                  │
│                                                                      │
│  [3A] format_instruction()   → Prompt Qwen ChatML                   │
│  [3B] tokenizer()            → max_length=2048                      │
│  [3C] dataset.map()          → batch tokenization                   │
│  [3D] TrainingArguments      → epochs, lr, fp16, cosine LR          │
│  [3E] trainer.train()        → Executa fine-tuning                  │
│  [3F] trainer.save_model()   → models/magistrado-themis-qlora        │
└─────────────────────────────────────────────────────────────────────┘
```

---

## GATE 1: Active Learning Loop (`dataset_builder.py`)

### Arquivos
- **Script:** `src/magistrado/dataset_builder.py`
- **Saída:** `dataset/forensic_dataset.jsonl`

### Eventos Seed Cobertos (51+ cenários)

| Label | Score | Optical | RF | Tamper | Classe |
|---|---|---|---|---|---|
| `autentico_todos_conformes` | 94.8 | 0.97 | 1.0 | 1.0 | AUTÊNTICO |
| `autentico_leve_desgaste` | 88.3 | 0.91 | 1.0 | 0.98 | AUTÊNTICO |
| `autentico_limite_aceite` | 85.1 | 0.86 | 1.0 | 0.95 | AUTÊNTICO |
| `suspeito_clonagem_optica` | 61.2 | 0.68 | 0.0 | 1.0 | SUSPEITO |
| `suspeito_violacao_parcial` | 73.5 | 0.79 | 1.0 | 0.72 | SUSPEITO |
| `critico_adulteracao_fisica` | 42.0 | 0.55 | 0.0 | 0.30 | SUSPEITO |
| `critico_lacre_destruido` | 28.0 | 0.45 | 0.0 | 0.10 | SUSPEITO |
| `fraude_sinistro_falsificado` | 15.0 | 0.25 | 0.0 | 0.10 | SUSPEITO |
| `borda_score_alto_nfc_falho` | 76.0 | 0.93 | 0.0 | 0.97 | SUSPEITO |

### Como Executar

```bash
# Modo batch (processa todos os eventos seed)
python src/magistrado/dataset_builder.py --batch

# Com augmentação de dados (gera 3 variantes por evento)
python src/magistrado/dataset_builder.py --batch --augment 3

# Modo interativo (adiciona entradas manuais)
python src/magistrado/dataset_builder.py
```

### Formato do Dataset

```json
{
  "_label": "suspeito_clonagem_optica",
  "input": {
    "gtid": "GD-0Z7F-4K2M",
    "metrics": {
      "trust_score": 61.2,
      "optical_similarity": 0.68,
      "rf_consistency": 0.0,
      "tamper_evidence": 1.0
    },
    "empresa": "FrotaTech Locações SA",
    "segmento": "frotista",
    "timestamp": "2026-06-30T22:00:00Z"
  },
  "output": "================...LAUDO COMPLETO...================"
}
```

---

## GATE 2: Fine-Tuning QLoRA (`fine_tune.py`)

### Arquivos
- **Script:** `src/magistrado/fine_tune.py`
- **Saída:** `models/magistrado-themis-qlora/`

### Configurações do Modelo

| Parâmetro | Valor | Justificativa |
|---|---|---|
| **Modelo base** | `Qwen/Qwen2.5-3B-Instruct` | Multilíngue PT-BR, pequeno, eficiente |
| **Quantização** | 4-bit NF4 (QLoRA) | Roda em GPU 8GB+ (VRAM econômica) |
| **LoRA rank (r)** | 16 | Equilíbrio capacidade/eficiência |
| **LoRA alpha** | 32 | = 2x rank (prática padrão) |
| **Target modules** | q, k, v, o proj | Atenção completa do transformer |
| **Seq length** | 2048 tokens | Cobre laudos completos (~1500 tokens) |
| **Formato prompt** | ChatML Qwen | `<\|im_start\|>user\n...<\|im_end\|>` |

### TrainingArguments Recomendados

| Parâmetro | Valor default | Para datasets maiores |
|---|---|---|
| `num_train_epochs` | 3 | 5 |
| `per_device_train_batch_size` | 4 | 2 (GPU menor) |
| `learning_rate` | 2e-4 | 1e-4 |
| `optimizer` | paged_adamw_32bit | — |
| `lr_scheduler_type` | cosine | — |
| `fp16` | True | True |
| `warmup_ratio` | 0.03 | 0.05 |

### Como Executar

```bash
# Instalação das dependências (GPU necessária)
pip install transformers peft trl bitsandbytes datasets torch accelerate

# Treinamento padrão (3 épocas)
python src/magistrado/fine_tune.py

# Personalizado
python src/magistrado/fine_tune.py \
    --epochs 5 \
    --batch_size 2 \
    --learning_rate 1e-4 \
    --output_dir models/magistrado-v2

# Em Google Colab Pro / RunPod — recomendado para primeira rodada
# Runtime: T4 (16GB VRAM) ou A100 para velocidade máxima
```

---

## Estado Atual do Pipeline

| Componente | Status | Observações |
|---|---|---|
| `server.py` — Motor de laudos | ✅ Completo | 125 entradas no dataset |
| `dataset_builder.py` — GATE 1 | ✅ Completo | 657 linhas, modo batch + interativo |
| `fine_tune.py` — GATE 2 | ✅ Completo | QLoRA ready, depende de GPU |
| `forensic_dataset.jsonl` | ✅ 533KB | 125 entradas com labels |
| Fine-tuning executado | ⬜ Pendente | Requer GPU 8GB+ ou Colab |
| Modelo treinado salvo | ⬜ Pendente | Aguarda GATE 2 execução |
| Integração com API | ⬜ GATE 3 | Endpoint `/v1/magistrado/laudo` |

---

## Infraestrutura de Treino Recomendada

Para executar o GATE 2, você precisará de:

- **Opção 1 (Gratuita):** Google Colab Pro+ com T4/A100
- **Opção 2 (Paga):** RunPod com A40 (~USD 0,40/h)
- **Opção 3 (Local):** RTX 3080 Ti (12GB VRAM) ou superior

**Estimativa de tempo de treino:** ~45 min (T4, 3 épocas, 125 exemplos)

---

*Symbeon Labs | GATE 2 — Fine-Tuning Pipeline*
