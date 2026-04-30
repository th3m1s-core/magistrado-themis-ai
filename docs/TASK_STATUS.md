# 📋 Status de Execução: Magistrado Themis

## 🔒 GATE 0 — ISOLAMENTO DO ATIVO
- [x] **0.1. Registro de Anterioridade**
- [x] **0.2. Claim Formal (RS Advogados)**
- [x] **0.3. Segregação de Código (magistrado-themis-core)**

---

## 🔬 GATE 1 — FUNDAÇÃO DE DADOS (EM EXECUÇÃO)
- [/] **1.1. Rodar `quick_validation.py`**
  - [x] Script localizado em `aoa-core`.
  - [ ] Aguardando captura de fotos reais/fakes pelo usuário.
- [/] **1.2. Ativar Active Learning Loop**
  - [x] API `aoa-core` (Inference) pronta para subir.
  - [ ] Implementar `dataset_builder.py` no Magistrado Core (NOVO).
- [ ] **1.3. Construir Dataset Forense do Magistrado**
  - [ ] Geração de pares `{evento_json} → {laudo_texto}`.

---

## 🧠 GATE 2 — FINE-TUNING DO MAGISTRADO
- [ ] Setup do ambiente QLoRA (Qwen-3B).
