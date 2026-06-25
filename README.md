# 🧠⚖️ Magistrado Themis — Motor de Inteligência Forense

**Classificação:** `CONFIDENCIAL — SEGREDO INDUSTRIAL`  
**Versão:** `v0.2.0`  
**Status:** `GATE 1 — Active Learning Loop Ativo`

---

## O que é

O **Magistrado Themis** é a camada de inteligência artificial do ecossistema GuardDrive™, responsável por:

1. **Geração de Laudos Técnico-Jurídicos Automatizados** — transforma métricas físico-ópticas do GuardTag™ em documentos forenses com embasamento legal (LGPD, CPC, Marco Civil, ICP-Brasil).
2. **Auditoria de Segurança de Ativos Integrados** — protege a propriedade intelectual da Symbeon Labs em integrações com frotas, seguradoras e parceiros externos.
3. **Active Learning Loop** — captura cada evento analisado em `dataset/forensic_dataset.jsonl` para treino futuro do modelo Qwen-3B (GATE 2).

---

## Arquitetura

```
src/magistrado/
├── server.py          # MCP stdio server (zero dependências externas)
│                      #   ├── generate_forensic_report() — geração de laudos
│                      #   └── run_security_check()       — auditoria de ativos
├── api.py             # FastAPI HTTP wrapper (para integração web)
├── dataset_builder.py # CLI de Active Learning (batch + interativo)
└── test_themis.py     # Testes end-to-end

dataset/
└── forensic_dataset.jsonl  # Pares evento→laudo para fine-tuning (VAULT PRIVATE)

docs/
├── EAP_MAGISTRADO_THEMIS.md          # Work Breakdown Structure
├── TECHNICAL_CONCEPT_ANTERIORITY.md  # Registro de anterioridade IP
└── governance/
    └── SYMBEON_GUARDDRIVE_LICENSING.md  # Acordo de licenciamento
```

---

## Ferramentas MCP disponíveis

### `gerar_laudo`
Gera um laudo técnico-jurídico completo baseado em métricas do GuardTag™.

**Input:**
```json
{
  "gtid": "GD-7A9F-2C4E",
  "score": 94.8,
  "optical_similarity": 0.97,
  "rf_consistency": 1.0,
  "tamper_evidence": 1.0,
  "empresa": "Seguradora Nacional de Frotas",
  "segmento": "seguradora"
}
```

**Output:** Laudo forense completo em linguagem natural com:
- Número de controle e timestamp
- Amparo legal (LGPD, CPC, Marco Civil, ICP-Brasil)
- Parecer técnico (AUTÊNTICO / SUSPEITO)
- Justificativa analítica detalhada
- Aviso de PI (Symbeon Labs)
- Assinatura criptográfica (SHA-256 + bloco simulado)

---

### `verificar_seguranca_ativo`
Audita a segurança de ativos e integrações externas, protegendo o IP da Symbeon Labs.

**Input:**
```json
{
  "app_domain": "https://api.parceiro.com.br",
  "target_market": "logistica",
  "exposed_keys": ["private_key_nfc"]
}
```

**Output:** Relatório de conformidade com:
- `safety_level`: SEGURO / ATENÇÃO / CRÍTICO
- `compliance_alerts`: lista de violações detectadas
- `recommendations`: ações corretivas recomendadas

---

## Como usar

### Como servidor MCP (integração com Antigravity IDE)
```json
// mcp_config.json — já configurado
{
  "mcpServers": {
    "magistrado-themis-ai": {
      "command": "python",
      "args": ["src/magistrado/server.py"],
      "env": {
        "THEMIS_ENV": "production",
        "SOVEREIGN_MODE": "true"
      }
    }
  }
}
```

### Como API HTTP (integração web)
```bash
pip install -r requirements.txt
cd src/magistrado
uvicorn api:app --host 0.0.0.0 --port 8001
# Documentação: http://localhost:8001/docs
```

### Como CLI de Active Learning
```bash
# Processar 5 eventos seed automaticamente
python src/magistrado/dataset_builder.py --batch

# Modo interativo para criar laudos manualmente
python src/magistrado/dataset_builder.py
```

---

## Roadmap (Gates)

| Gate | Status | Objetivo |
|------|--------|----------|
| **GATE 0** | ✅ Concluído | Isolamento de IP e registro de anterioridade |
| **GATE 1** | 🟡 Em andamento | Dataset de eventos forenses (Active Learning) |
| **GATE 2** | ⬜ Pendente | Fine-tuning Qwen-3B com QLoRA |
| **GATE 3** | ⬜ Pendente | Integração oficial com UEAP + assinatura Ed25519 |
| **GATE 4** | ⬜ Pendente | Depósito INPI + produto comercial B2B |

---

## ⚠️ Regras de Operação

> **NUNCA publicar em repositório público antes do GATE 4 (depósito de patente).**  
> O dataset `forensic_dataset.jsonl` deve permanecer em `10_VAULT_PRIVATE` ou ar-gapped (SEED#2).  
> A licença de uso pela GuardDrive Tech é exclusiva para **Logística e Segurança de Carga**.

---

*Propriedade intelectual da Symbeon Labs. Licenciado para GuardDrive Tech.*  
*Magistrado Themis™ é uma marca registrada — Centelha III Execution Phase.*
