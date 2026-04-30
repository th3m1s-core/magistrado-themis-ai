# 🛡️ Protocolo de Instalação Forense: GuardTag 2.0
**Versão:** `2.0.1 — Standard Operating Procedure (SOP)`
**Referência:** `th3m1s-core / Symbeon Labs`

Este protocolo define os procedimentos obrigatórios para a instalação física do selo GuardTag 2.0 em ativos móveis. A adesão estrita a estes passos é necessária para que o **Magistrado Themis** valide a integridade do dispositivo e emita laudos forenses de alta confiança.

---

## 🏗️ 1. Preparação do Sítio de Instalação
1.  **Limpeza Química:** A área interna do para-brisa deve ser limpa com álcool isopropílico 70% para remoção de gorduras, poeira e resíduos de silicone.
2.  **Secagem Absoluta:** Aguardar a evaporação total antes da aplicação. Umidade residual compromete a camada de adesivo *Tamper-Evident*.
3.  **Auditoria de Película:** Verificar se não há películas metálicas (insulfilm) ou serigrafias cerâmicas que possam interferir na leitura RFID UHF ou na transparência óptica necessária para a IA.

## 📍 2. Posicionamento Estratégico
- **Local:** Face interna do para-brisa, preferencialmente na área superior central ou lateral.
- **Alinhamento:** Posicionamento vertical com tolerância máxima de **±15°** para garantir a angulação ideal de captura pelo aplicativo AOA-Core.

## 🖐️ 3. Aplicação e Ativação Física
1.  **Remoção do Liner:** Retirar o liner protetor sem tocar na face adesiva.
2.  **Pressão de Contato:** Pressionar firmemente o selo contra o vidro por **10 segundos** ininterruptos. Isso garante a ativação total do adesivo de alta aderência e resistência térmica.
3.  **Verificação de Bolhas:** Confirmar visualmente se não há bolhas de ar sobre o QR Code ou sobre o Marcador Óptico (AOA).

## 🧠 4. Vinculação Forense (Registro Digital)
Após a aplicação física, o instalador deve:
1.  **Captura Inicial (Master OFP):** Utilizar o App GuardDrive para realizar a primeira captura óptica. O Magistrado Themis salvará este "Snapshot de Nascimento" como a verdade absoluta do selo.
2.  **Handshake Criptográfico:** Validar a resposta do chip NTAG 424 DNA para garantir que a antena não foi danificada durante a pressão.
3.  **Selagem Logística:** Vincular o GTID (ID do Selo) à placa/chassi do veículo no Vault Soberano.

## ⚠️ 5. Indicadores de Violação
- **Física:** Aparecimento da palavra **"VOID"** ou fragmentação do substrato PET.
- **Digital:** Divergência no *Trust Score* superior a 15% em relação ao Master OFP original.
- **RF:** Falha na resposta da assinatura criptográfica dinâmica (SUN).

---
*Este documento é parte integrante do sistema de governança GuardDrive. Qualquer desvio neste protocolo invalida a custódia do evento físico.*
