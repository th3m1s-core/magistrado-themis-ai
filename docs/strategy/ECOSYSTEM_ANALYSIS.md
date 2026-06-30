# 🦅 GuardDrive — Análise Completa do Ecossistema

> **Documento interno | Versão: 2026-06-30 | Confidencial**

---

## 1. Visão Geral: O Que é o GuardDrive

O GuardDrive é uma **infraestrutura de mobilidade soberana** — um sistema que transforma eventos físicos de veículos em **evidências auditáveis e economicamente valiosas**. 

O produto não é um rastreador. É uma **cadeia de custódia digital** para frotas, seguradoras e editais públicos.

**O problema que resolve:** R$ 19 bilhões em fraudes logísticas anuais no Brasil. Isso inclui:
- Falso frete (veículo reporta presença em porto sem estar lá)
- Clonagem de placas e selos
- Adulteração de tacógrafos
- Jammers de GPS em rodovias
- Litígios por falta de prova física admissível em juízo

---

## 2. Arquitetura em Camadas (O Stack Completo)

```
┌─────────────────────────────────────────────────────────┐
│  L4 — ECONOMIA          BaaT / GuardScore / GST Token   │
│         ↑               ESG Score → Token Mintado       │
├─────────────────────────────────────────────────────────┤
│  L3 — APLICAÇÃO         GuardDrive Pilot (Digital Twin) │
│         ↑               Intelligence Hub (B2B)          │
│         ↑               Landing Page (Captação)         │
├─────────────────────────────────────────────────────────┤
│  L2 — PROTOCOLO         Symbeon Core                    │
│         ↑               ZK-Privacy + ECDSA + DAE        │
│         ↑               Magistrado Themis (IA Forense)  │
├─────────────────────────────────────────────────────────┤
│  L1 — FÍSICO            GuardTag Hardware               │
│                         7 camadas de autenticação       │
│                         PoPE (Prova de Realidade Física)│
└─────────────────────────────────────────────────────────┘
```

### Como as camadas se comunicam

```
[Veículo com GuardTag]
        │  WebSocket / BLE / NFC
        ▼
[GuardTagClient.ts] ──── captura evento multimodal
        │  JSON + SHA-256
        ▼
[seve_symbeon_bridge.py] ──── aplica pesos éticos (SEVE)
        │  ECDSA signature
        ▼
[Protocolo Symbeon L2] ──── gera PoPE (Prova Criptográfica)
        │  Registro imutável
        ▼
[Magistrado Themis] ──── gera laudo técnico-jurídico
        │  PDF/texto estruturado
        ▼
[Intelligence Hub / Pilot] ──── exibe para operador/seguradora
        │  ESG Score calculado
        ▼
[GST Token] ──── recompensa comportamento seguro
```

---

## 3. O Intelligence Hub — O Que É e Como Funciona

### 3.1 Definição Estratégica

O Intelligence Hub **não é um produto para o motorista**. É a **central de inteligência B2B** da GuardDrive — voltada para:

| Usuário | O que vê no Hub |
|---|---|
| **Equipe GuardDrive** | Leads captados, análise de mercado, Data Room |
| **Escritório RS Advogados** | Documentos estratégicos, minutas, NDA aceitos |
| **Adriano (CTO/Parceiro)** | Dados técnicos, integrações, laudos gerados |
| **Seguradoras (futuro)** | Dashboard de sinistros validados por IA |

### 3.2 O que está construído hoje

**Frontend (Next.js 15 — Vercel)**
```
https://guarddrive-intelligence-hub.vercel.app
  ├── /login          ← autenticação JWT
  ├── /register       ← cadastro de usuários
  └── /dashboard      ← central de inteligência
       ├── Overview   ← métricas, segmentos, leads recentes
       ├── Leads      ← tabela completa com origem (landing/interno)
       ├── Data Room  ← documentos estratégicos (6 docs)
       ├── Inteligência de Mercado ← TAM/SAM/SOM, oportunidades
       └── Configurações ← perfil + sistema
```

**Backend (FastAPI — pendente Railway)**
```
/api/auth/login         ← JWT login
/api/auth/register      ← criar usuário
/api/leads              ← CRUD de leads (autenticado)
/api/leads/public       ← recebe leads da Landing Page
/api/leads/stats        ← estatísticas
/api/companies          ← empresas cadastradas
/api/market-data        ← dados de mercado
/api/dashboard/overview ← resumo geral
```

### 3.3 Fluxo de dados hoje

```
Landing Page (visitante)
    │  preenche formulário de contato
    ▼
POST /api/leads/public (backend Landing Page)
    │  httpx assíncrono → não bloqueia
    ▼
Intelligence Hub /api/leads/public
    │  auto-cria empresa + salva lead
    ▼
Dashboard → seção Leads
    │  equipe GuardDrive vê e qualifica
    ▼
Reunião / NDA / Piloto
```

---

## 4. O GuardTag — Como Funciona e Como Vamos Programá-lo

### 4.1 O que é o GuardTag

O GuardTag é o **ancla de hardware** do ecossistema — o objeto físico instalado no veículo que torna impossível fraudar a identidade do ativo.

### 4.2 As 7 Camadas de Autenticação

```
┌────────────────────────────────────────────────────────────┐
│  L1  RFID / NFC (NXP NTAG 424 DNA)                        │
│       → Autenticação em docas, leitura por celular        │
│       → Chave criptográfica AES-128 gravada em hardware   │
│                                                            │
│  L2  BLE 5.0                                              │
│       → Leitura passiva em pedágios, rodovias             │
│       → Range: ~100m sem linha de visada                  │
│                                                            │
│  L3  IR TX/RX (Infravermelho)                             │
│       → Imune a jammers de RF                             │
│       → Funciona em ambientes metálicos (contêineres)     │
│                                                            │
│  L4  Geolocalização                                       │
│       → Metadados de antenas de borda                     │
│       → Triangulação mesmo sem GPS ativo                  │
│                                                            │
│  L5  OBD-II Integration                                   │
│       → Saúde do motor atrelada à ignição física          │
│       → Impossível reportar presença com motor desligado  │
│                                                            │
│  L6  TOTP Visual (QR/Code)                               │
│       → Token de 30s para leitura humana                 │
│       → Backup quando eletrônica falha                    │
│                                                            │
│  L7  Assinatura Óptica Atômica (AOA)                     │
│       → IA lê micro-geometria física do adesivo           │
│       → Padrão DTM único por unidade                      │
│       → Destruído se o adesivo for removido               │
└────────────────────────────────────────────────────────────┘
```

**Princípio fundamental:** Se uma camada for atacada (jammer derruba BLE+NFC), o sistema triangula as camadas restantes para gerar o PoPE com confiança reduzida — mas nunca silencia.

### 4.3 Os Dois Modelos de Hardware

#### GuardTag V1 — Passive MVP (FOCO ATUAL)

```
Componentes:
  ├── Substrato PET (60mm diâmetro, 0.8mm espessura)
  ├── Adesivo Tamper-Evident (destrói padrão ao remover)
  ├── Inlay Criptográfico: NXP NTAG 424 DNA
  │     └── AES-128 + CMAC authentication
  ├── DTM Visual (micro-geometria lida por câmera)
  ├── Tinta OVI (muda de cor sob ângulo diferente)
  └── Acabamento PU UV-resistant (-40°C a +85°C)

BOM Target: US$ 1.28 (R$ 13–17 Brasil)
Caso de uso: Identidade criptográfica, controle de pátio,
             prova de realidade via celular
```

#### GuardTag V2 — Active Edge (FASE SEGUINTE)

```
Componentes:
  ├── ESP32-S3 (dual-core 240MHz, WiFi + BLE 5.0)
  ├── Transmissores IR TX/RX
  ├── Bateria CR2032 ou OBD-II power rail
  ├── FreeRTOS (Sistema operacional embarcado)
  └── Firmware C++ com SDK TypeScript bridge

BOM Target: US$ 15–25
Caso de uso: Pedágios Free-Flow, imunidade jammers RF,
             telemetria contínua em rodovias
```

### 4.4 Como Vamos Programar o GuardTag

#### Camada 1: Firmware (ESP32 — C++ / FreeRTOS)

O firmware já existe em `GuardTag/firmware/`. Ele roda no ESP32-S3 e gerencia:

```cpp
// Estrutura geral do firmware
loop() {
  1. Captura evento físico (botão, OBD, NFC read)
  2. Lê sensores (BLE scan, IR RX, GPS)
  3. Gera GuardTagEvent {
       device_id, timestamp, layers[], raw_data
     }
  4. Assina com ECDSA (chave gravada no eFuse do ESP32)
  5. Transmite via WebSocket / BLE para GuardTagClient.ts
}
```

**Próximos passos no firmware:**
- Implementar modo low-power (deep sleep entre eventos)
- Integrar OBD-II via UART (ELM327 ou customizado)
- Adicionar validação TOTP de 30s (layer L6)

#### Camada 2: SDK TypeScript (Integradores)

```typescript
// GuardTag/sdk/src/GuardTagClient.ts
// Já implementado — conecta via WebSocket

const client = new GuardTagClient('ws://localhost:8765');

client.on('event', (event: GuardTagEvent) => {
  // Evento chega aqui com todas as camadas
  // Envia para o Symbeon Bridge para assinar
  symbeonBridge.validate(event);
});
```

**Próximos passos no SDK:**
- Publicar no NPM como `@guarddrive/tag-sdk`
- Adicionar suporte BLE via Web Bluetooth API
- Implementar fallback NFC para mobile

#### Camada 3: Protocolo Symbeon (Assinatura e Validação)

```python
# symbeon-protocol/core/seve_symbeon_bridge.py
# Já implementado

bridge = SevSymbeonBridge(domain="logistics")
bridge.inject_seve_ethics({
    "privacy": 0.3,
    "safety": 0.9,   # > 0.8 → contexto "emergency"
    "forensics": 0.8
})

result = bridge.validate_and_sign({
    "gtid": "GD-7A9F-2C4E",
    "speed": 87.4,
    "layers_active": [1, 2, 4, 7],
    "tamper_evidence": 1.0
})
# result = { status: "validated", signature: "0x...", hash: "AOA-..." }
```

#### Camada 4: Magistrado Themis (Laudo Automático)

Quando o evento chega validado pelo Symbeon, o Magistrado gera automaticamente o laudo:

```python
# magistrado-themis-core/src/magistrado/server.py
report = generate_forensic_report({
    "gtid": "GD-7A9F-2C4E",
    "score": 94.8,
    "optical_similarity": 0.97,
    "rf_consistency": 1.0,
    "tamper_evidence": 1.0,
    "empresa": "Seguradora Nacional de Frotas",
    "segmento": "seguradora"
})
# Saída: Laudo com número de controle, amparo legal (LGPD, CPC, ICP-Brasil),
#         parecer AUTÊNTICO/SUSPEITO, hash SHA-256, bloco simulado
```

---

## 5. Roadmap de Programação do GuardTag

### GATE 0 — ✅ Concluído
- Firmware base ESP32 funcionando
- SDK TypeScript com WebSocket
- Protocolo Symbeon com ECDSA
- AOA com SHA-256 chaining

### GATE 1 — 🟡 Em Andamento
- Dataset forense do Magistrado Themis (`forensic_dataset.jsonl`)
- Firmware OBD-II integration
- V1 Passive Tag: validação física do adesivo NXP NTAG 424

### GATE 2 — ⬜ Próximo
- Fine-tuning Qwen-3B com dataset do Magistrado (QLoRA)
- SDK público NPM (`@guarddrive/tag-sdk`)
- App mobile para leitura NFC do V1

### GATE 3 — ⬜ Futuro
- Integração UEAP (assinatura Ed25519)
- API pública para seguradoras
- Dashboard de laudos em tempo real no Intelligence Hub

### GATE 4 — ⬜ Produto Comercial
- Depósito INPI
- Linha de fabricação V1 (BOM R$ 13–17)
- Contratos B2B com frotas/seguradoras

---

## 6. O que Falta para Fechar o Ciclo Completo

| Componente | Status | Próxima ação |
|---|---|---|
| GuardTag V1 (adesivo) | 🟡 Prototipagem | Fabricar lote piloto 100 unidades |
| GuardTag V2 (ESP32) | 🟡 Firmware base | Integrar OBD-II + testar em campo |
| SDK TypeScript | ✅ Implementado | Publicar no NPM |
| Symbeon Protocol | ✅ Beta | Integrar com Intelligence Hub |
| Magistrado Themis | 🟡 GATE 1 | Fine-tuning (GATE 2) |
| Intelligence Hub (frontend) | ✅ Live (Vercel) | Conectar backend Railway |
| Intelligence Hub (backend) | 🟡 Pronto, sem host | Deploy no Railway |
| Landing Page | ✅ Live (Vercel) | — |
| GST Token (L4) | ⬜ Design | Aguarda GATE 3 |

---

## 7. O que o Intelligence Hub Precisa para Completar

### Imediato (esta semana)
1. **Backend no Railway** — Deploy do FastAPI com admin seed
2. **Conectar `NEXT_PUBLIC_API_URL`** no Vercel → URL do Railway
3. **Testar login** com `admin@guarddrive.tech / GuardDrive@2026!`

### Curto prazo (próximas 2 semanas)
4. **Endpoint `/api/laudos`** — receber laudos do Magistrado Themis
5. **Seção "Laudos"** no dashboard — visualizar laudos gerados em tempo real
6. **Gráficos reais** (Recharts) substituindo mock data

### Médio prazo
7. **PostgreSQL** — migrar do mock em memória
8. **Autenticação por roles** — admin vê tudo, analyst vê leads
9. **API para seguradoras** — acesso externo a laudos validados

---

*GuardDrive Tech | Symbeon Labs | Centelha III Execution Phase*
