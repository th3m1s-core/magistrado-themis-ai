# 🧠⚖️ Magistrado Themis — Estratégia do Modelo Treinado e Plano de Dados
## O Ativo que Será Criado e Como Chegar Lá

> **Classificação:** Estratégia de IP | Symbeon Labs
> **Data:** 2026-06-30

---

## PARTE 1 — O QUE VOCÊ TERÁ NAS MÃOS

### 1.1 O Ativo Técnico: `magistrado-themis-qlora-v1`

Ao final do GATE 2, você terá um **arquivo de adaptadores LoRA** (~150–300MB) que transforma
o Qwen-2.5-3B genérico em um **perito forense digital especializado em direito brasileiro**.

```
Qwen-2.5-3B (genérico)         →     Magistrado Themis v1 (especializado)
─────────────────────────────────────────────────────────────────────────
"Escreva um e-mail"            →     "Emita um laudo jurídico forense"
Qualquer domínio               →     Forense veicular + LGPD + CPC
Resposta casual                →     Estrutura de laudo perito homologável
Sem lastro jurídico            →     Hexágono Legislativo embutido no modelo
Depende de APIs externas       →     Roda offline, edge computing, sem OpenAI
```

### 1.2 O que o Modelo Consegue Fazer

Dada uma entrada como esta:

```json
{
  "gtid": "GD-0Z7F-4K2M",
  "trust_score": 61.2,
  "optical_similarity": 0.68,
  "rf_consistency": 0.0,
  "tamper_evidence": 1.0,
  "empresa": "FrotaTech Locações SA"
}
```

O modelo produz autonomamente:

```
>>> [ SUSPEITO ] <<<
Nível de Confiança: 61.2/100

Análise: Similitude óptica abaixo do limiar (0.68 vs ≥ 0.85 esperado).
Ausência de sinal RF/NFC — indica possível reprodução por impressão.
Divergência nas métricas sugere clonagem óptica ou remoção física do selo.

Amparo Legal: LGPD Art. 46, CPC Art. 411, Marco Civil Art. 10.
Recomendação: Bloqueio imediato, inspeção física obrigatória.

Selo Criptográfico: 0x8ae52937...
```

### 1.3 Progressão de Valor do Ativo

```
HOJE          Motor rule-based (server.py)
              → Laudo determinístico, previsível, sem aprendizado
              → Valor: prova de conceito

GATE 2        Modelo fine-tunado (QLoRA)
              → Laudo generativo, adaptável, proprietário
              → Valor: ativo de IP diferenciado, patenteável

GATE 3        API assinada + integração UEAP
              → Produto comercial, admissível juridicamente
              → Valor: R$ 500K–2M (licenciamento B2B)

GATE 4        Patente INPI depositada
              → Monopólio legal sobre o método
              → Valor: R$ 2M–8M (valuation incremental)
```

### 1.4 O que NÃO Será (Expectativas Corretas)

> [!NOTE]
> Com 125 exemplos sintéticos e 3 épocas, o modelo v1 vai:
> - ✅ Gerar laudos estruturados e coerentes
> - ✅ Usar o vocabulário jurídico correto (LGPD, CPC, ICP-Brasil)
> - ✅ Replicar o padrão de raciocínio forense
> - ⚠️ Às vezes ser verboso ou repetitivo
> - ❌ Não estará pronto para produção jurídica real sem supervisão humana

Isso é **esperado e correto** para um modelo v1. O GATE 3 corrige isso com dados reais.

---

## PARTE 2 — PLANO DE OBTENÇÃO DE DADOS

> [!IMPORTANT]
> O dataset de pares evento→laudo é o **ativo mais sensível de toda a operação**.
> Quem tiver esses dados + o modelo treinado tem a empresa. Armazenar exclusivamente
> no `SEED#2` (ar-gap) e nunca em repositório público.

### 2.1 Hierarquia de Qualidade dos Dados

```
Nível 1 — Dados Sintéticos (AGORA)
  ✅ Custo zero
  ✅ Cobertura total de cenários
  ⚠️ Modelo aprende "o que eu programei", não "o que acontece no mundo"

Nível 2 — Dados Reais Simulados (GATE 1, semanas 1–4)
  ✅ Baseados em eventos físicos reais
  ✅ Validados por humano antes de entrar no dataset
  ✅ Diversidade de situações imprevisíveis

Nível 3 — Dados Reais Homologados (GATE 3, semanas 13–20)
  ✅ Revisados por advogado (RS Advogados)
  ✅ Laudos aprovados para uso em juízo
  ✅ O modelo aprende a linguagem que juízes aceitam
```

---

### 2.2 Fase A — Dados Sintéticos (Status: ✅ Concluído)

**O que temos:** 125 entradas no `forensic_dataset.jsonl`
**Como foram gerados:** Motor rule-based (`server.py`) sobre 51 eventos seed
**Cobertura de cenários:**

| Categoria | Exemplos | % do Dataset |
|---|---|---|
| Autêntico — todos conformes | 18 | 14% |
| Suspeito — clonagem óptica | 22 | 18% |
| Suspeito — violação física | 20 | 16% |
| Crítico — adulteração total | 16 | 13% |
| Edge cases — limiar exato | 14 | 11% |
| Outros cenários mistos | 35 | 28% |

**Limitação:** O modelo aprende a replicar o motor rule-based, não a raciocinar sobre casos novos.

---

### 2.3 Fase B — Dados Reais com Selos Físicos (GATE 1, semanas 1–4)

**Objetivo:** Fotografar selos GuardTag reais e selos falsos para criar eventos baseados em
medições físicas reais — não simuladas.

#### Protocolo de Coleta

**Material necessário:**
- 1 smartphone com app GuardDrive (câmera + NFC)
- 30–50 selos GuardTag originais (de produção)
- 10–15 reproduções (print A4, cópia xerox, foto de tela)
- 5–8 selos danificados fisicamente (arranhados, recortados)

**Procedimento por evento:**
```
1. Fotografar o selo em luz natural (ângulo 45°, distância 15cm)
2. Escanear NFC com o app (gera rf_consistency automático)
3. Inspecionar integridade física (tamper_evidence = 0.0–1.0 manual)
4. App calcula optical_similarity via OFP
5. Registrar empresa/segmento/contexto do teste
6. Salvar o evento JSON gerado pelo app
```

**Gate de saída (validação dos dados):**
```
real vs real:  optical_similarity ≥ 0.85  (média esperada: 0.92+)
real vs fake:  optical_similarity ≤ 0.70  (média esperada: 0.55–0.68)
```

Se esses limiares não forem atingidos, a câmera ou o OFP precisa de ajuste antes de continuar.

#### Quantidade Mínima para GATE 2

| Tipo de Evento | Quantidade Mínima | Ideal |
|---|---|---|
| Autêntico (foto real) | 30 | 50 |
| Suspeito (cópia impressa) | 10 | 15 |
| Crítico (lacre destruído) | 5 | 10 |
| Edge case (desgastado) | 5 | 10 |
| **Total** | **50** | **85** |

> **Com 50 eventos reais + 125 sintéticos = ~175 entradas totais**
> Isso já muda significativamente a qualidade do modelo.

---

### 2.4 Fase C — Dados Jurídicos Revisados (GATE 3, semanas 13–20)

**Objetivo:** Ter laudos revisados por advogado — linguagem, estrutura e amparo legal
validados para admissibilidade em juízo.

#### Parceria com RS Advogados

**Proposta de trabalho:**
1. Apresentar 10–20 laudos gerados pelo modelo v1
2. Advogado faz correções: linguagem, artigos legais, estrutura do parecer
3. Par corrigido entra no dataset como **gold standard** (peso 10x no treino)
4. Dataset final tem: sintético + real + jurídico = modelo jurídico v2

**Custo estimado:** 2–4h de consultoria jurídica (~R$ 600–1.200)
**Retorno:** Modelo que gera laudos admissíveis em juízo sem revisão humana

#### Tipos de Laudos a Revisar

| Cenário | Importância para o Mercado |
|---|---|
| Sinistro com fraude de lacre (seguradora) | Alta — R$ bilhões em fraude/ano |
| Veículo com NFC clonado (contencioso) | Alta — admissibilidade como prova |
| Roubo com adulteração de identificação | Muito Alta — processo criminal |
| Auditoria de frota (compliance DETRAN) | Média — regulatório |

---

### 2.5 Fase D — Active Learning Contínuo (Pós-GATE 3)

Após o produto estar em operação, cada laudo gerado e **revisado por um operador** pode
ser automaticamente adicionado ao dataset para treino contínuo.

```
Operador escaneia → App gera laudo → Operador confirma/corrige → Dataset cresce
                                                                        ↓
                                                              Re-treinamento mensal
                                                              Modelo melhora com uso
```

Isso cria um **fosso competitivo crescente**: quanto mais o sistema é usado, mais dados
exclusivos ele acumula, e mais difícil fica de ser replicado por um concorrente.

---

## PARTE 3 — CRONOGRAMA DE EXECUÇÃO

```
SEMANA 1–2   → Rodar GATE 2 no Colab (dados sintéticos)
               Ter modelo v1 funcionando
               Meta: checklist de qualidade ≥ 70%

SEMANA 3–4   → Coleta de dados físicos reais (Fase B)
               30–50 eventos reais fotografados e medidos
               Expandir dataset para 175+ entradas

SEMANA 5–8   → Re-treinar modelo com dados reais (v1.1)
               Meta: checklist de qualidade ≥ 85%
               Demo em vídeo: evento → laudo em 2 segundos

SEMANA 9–12  → Integração API FastAPI (GATE 3)
               Endpoint /v1/magistrado/laudo operacional
               Assinatura Ed25519 em cada laudo

SEMANA 13–16 → Revisão jurídica com RS Advogados
               Dataset gold standard (20–30 laudos revisados)
               Re-treino com peso aumentado nos laudos jurídicos (v2)

SEMANA 17–20 → Testes jurídicos em casos reais
               Ajuste fino de linguagem
               Preparação para depósito INPI

MÊS 6+       → Depósito de patente (GATE 4)
               Produto comercial no mercado
```

---

## PARTE 4 — CÁLCULO DO VALOR DO ATIVO

### Por que o modelo fine-tunado tem valor de IP

Um modelo fine-tunado **não é substituível** pelo prompt engineering. A diferença é:

| Abordagem | Custo por laudo | Dependência | Replicável |
|---|---|---|---|
| Prompt no GPT-4 | ~R$ 0,50–2,00 | OpenAI/Gemini | Imediata |
| Motor rule-based (atual) | R$ 0,001 | Nenhuma | Fácil (lógica pública) |
| **Modelo fine-tunado** | **R$ 0,002** | **Nenhuma** | **Impossível sem os dados** |

O valor do modelo não é o código — é o **dataset exclusivo** que o tornou especialista.
Esse dataset é gerado pela operação dos selos GuardTag, que só você tem acesso.

### Valuation do Ativo

| Métrica | Estimativa |
|---|---|
| Custo de replicação por concorrente | R$ 800K–2M (coletar dados + treinar) |
| Receita recorrente com 50 escritórios | R$ 1.5M ARR |
| Licenciamento para GuardDrive (royalty) | R$ 200K–400K/ano |
| Valuation do ativo de IP isolado | **R$ 2M–8M** |

---

*Symbeon Labs | Magistrado Themis — Estratégia de Modelo e Dados*
*CONFIDENCIAL — SEGREDO INDUSTRIAL*
