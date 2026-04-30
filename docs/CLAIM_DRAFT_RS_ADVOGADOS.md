# 🛡️ Rascunho de Claim de Patente — Magistrado Themis
**Status:** `DRAFT v1.0 — Para revisão com RS Advogados`

## 🎯 Reivindicação Principal (Software/Método)

**Objeto:** Método computadorizado para emissão automatizada de laudos forenses de autenticidade baseados em inteligência artificial.

**Características Inovadoras:**
1.  **Ingestão Multimodal de Eventos:** O sistema recebe como entrada um objeto de dados estruturado (formato UEAP) contendo métricas ópticas (OFP), radiofrequência (NFC/RFID) e integridade física (Tamper Detection).
2.  **Motor de Raciocínio Jurídico (LLM Fine-tuned):** Utiliza um modelo de linguagem de grande escala, especificamente treinado em um dataset de jurisprudência técnica e normas de cadeia de custódia, para interpretar as métricas de entrada.
3.  **Conversão Semântica Forense:** O método converte o "Trust Score" numérico em uma narrativa jurídica formal em linguagem natural, citando as discrepâncias técnicas detectadas.
4.  **Assinatura de Autoria Algorítmica:** O laudo resultante é selado com uma assinatura criptográfica (Ed25519) vinculada à identidade imutável do veículo/objeto, garantindo o não-repúdio da auditoria.

## 🔗 Diferenciação do GuardTag (Hardware)
- Enquanto o GuardTag reivindica o **hardware de captura** e a **geometria do selo**, o Magistrado Themis reivindica o **processo de interpretação jurídica** do dado gerado.
- Isso permite o licenciamento do Magistrado para outros sistemas de rastreabilidade que não usam o hardware GuardTag.

## ⚖️ Fundamentação Legal (LPI 9.279/96)
- **Novidade:** Não existem sistemas que unificam captura física + interpretação jurídica automática em borda (Edge).
- **Atividade Inventiva:** A transposição de métricas de visão computacional para laudos jurídicos formais via LLM não é óbvia para um técnico no assunto.
- **Aplicação Industrial:** Aplicável em seguradoras, fiscalização aduaneira e gestão de frotas.

---
*Documento preparado por Antigravity (AI Architect) sob supervisão de João (Arquiteto do Ecossistema).*
