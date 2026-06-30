# 📡 Magistrado Themis — API de Laudos e Auditoria (v0.2.0)
## Documentação dos Endpoints do Hub de Inteligência

> **Classificação:** Técnico | Symbeon Labs
> **Data:** 2026-06-30

---

## Visão Geral

A API do Magistrado Themis é exposta via **FastAPI** e serve como o ponto de entrada programático para a validação forense e auditoria de IP no ecossistema Symbeon.

O servidor pode ser iniciado localmente via:
```bash
python src/magistrado/api.py
```
*Porta padrão:* `8000`

---

## 1. POST `/v1/magistrado/laudo`

Gera um laudo técnico-jurídico detalhado a partir de métricas de telemetria física-óptica e assina digitalmente o resultado usando a curva elíptica **Ed25519** (não-repúdio).

### Requisição (Payload JSON)

```json
{
  "gtid": "GD-0Z7F-4K2M",
  "score": 61.2,
  "optical_similarity": 0.68,
  "rf_consistency": 0.0,
  "tamper_evidence": 1.0,
  "empresa": "FrotaTech Locações SA",
  "segmento": "frotista"
}
```

#### Parâmetros:
* `gtid` (string): Identificador único do ativo veicular sob cadeia de custódia.
* `score` (float): Pontuação de confiança unificada (0.0 a 100.0).
* `optical_similarity` (float): Similaridade de microtextura óptica (OFP) obtida (0.0 a 1.0).
* `rf_consistency` (float): Consistência do chip NFC criptográfico (1.0 = Conforme, 0.0 = Ausente/Divergente).
* `tamper_evidence` (float): Score do lacre físico contra violação (0.0 a 1.0, onde 1.0 é intacto).
* `empresa` (string): Nome da empresa parceira operando a medição.
* `segmento` (string): Tipo de parceiro (`frotista`, `seguradora`, `outro`).

### Resposta (JSON)

```json
{
  "laudo": "================================================================================\n          LAUDO TÉCNICO-JURÍDICO AUTOMATIZADO — INICIATIVA GUARDDRIVE™\n...",
  "status": "ok",
  "signature": "8a38c291bd8fa7ec...",
  "public_key": "9cf17d23be8fa290...",
  "block_num": 194302
}
```

#### Estrutura de Retorno:
* `laudo` (string): Relatório pericial completo em formato textual, contendo metodologia, fundamentação legal (LGPD, Marco Civil, CPC) e parecer.
* `status` (string): Estado operacional (`ok`).
* `signature` (string, hex): Assinatura Ed25519 gerada sobre o texto do laudo.
* `public_key` (string, hex): Chave pública utilizada para verificação da assinatura.
* `block_num` (int): Bloco da L2 (Protocolo Symbeon) simulado no registro.

---

## 2. POST `/v1/magistrado/security_check`

Audita de forma automática a conformidade do mercado-alvo e chaves de segurança expostas por ativos integrados de terceiros, garantindo a proteção de IP da Symbeon Labs.

### Requisição (Payload JSON)

```json
{
  "app_domain": "https://api.frotapartner.com.br",
  "target_market": "finanças",
  "exposed_keys": ["private_key_nfc", "session_key_rfid"]
}
```

### Resposta (JSON)

```json
{
  "compliance_level": "ATENÇÃO",
  "issues_detected": [
    "AVISO DE MERCADO: O mercado-alvo 'finanças' difere da concessão de uso exclusiva para 'Mobilidade e Telemetria Veicular' concedida pela Symbeon Labs. Recomenda-se formalizar aditivo contratual com o escritório RS Advogados.",
    "VAZAMENTO DE CHAVE CRÍTICA: Chave vulnerável exposta em ambiente de terceiros: private_key_nfc"
  ],
  "timestamp": "2026-06-30T23:15:00.123456Z"
}
```

#### Estrutura de Retorno:
* `compliance_level` (string): Nível de risco (`SEGURO`, `ATENÇÃO`, `CRÍTICO`).
* `issues_detected` (list): Lista de alertas de conformidade contratual ou vazamentos criptográficos detectados.
* `timestamp` (string): Data e hora da checagem.

---

*Symbeon Labs | Magistrado Themis API*
*CONFIDENCIAL — SEGREDO INDUSTRIAL*
