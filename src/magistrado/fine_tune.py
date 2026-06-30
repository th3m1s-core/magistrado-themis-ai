# -*- coding: utf-8 -*-
"""
Magistrado Themis — Fine-Tuning Script (GATE 2)
Fine-tuning do Qwen-2.5-3B-Instruct com QLoRA para laudos forenses

Requisitos:
- GPU com 8GB+ VRAM (ou Colab Pro+ / RunPod)
- transformers, peft, trl, bitsandbytes, torch

Uso:
    python fine_tune.py --epochs 3 --batch_size 4 --learning_rate 2e-4
"""
import os
import json
import argparse
import torch
from datetime import datetime
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    BitsAndBytesConfig,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training


# ── Configurações ─────────────────────────────────────────────────────────────
MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"
DATASET_PATH = "dataset/forensic_dataset.jsonl"
OUTPUT_DIR = "models/magistrado-themis-qlora"
MAX_SEQ_LENGTH = 2048


def load_dataset(path: str) -> Dataset:
    """Carrega o dataset forense do arquivo JSONL."""
    examples = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            # Formata para fine-tuning instruction-tuning
            input_text = format_instruction(data["input"])
            output_text = data["output"]
            examples.append({"input": input_text, "output": output_text})
    
    return Dataset.from_list(examples)


def format_instruction(event: dict) -> str:
    """Formata o evento de entrada como instrução para o modelo."""
    metrics = event.get("metrics", {})
    return f"""Analise o seguinte evento forense do GuardTag e emita um laudo técnico-jurídico.

GTID: {event.get('gtid', 'N/A')}
Empresa: {event.get('empresa', 'N/A')}
Segmento: {event.get('segmento', 'N/A')}

Métricas de Autenticidade:
- Trust Score: {metrics.get('trust_score', 0):.1f}/100
- Similaridade Óptica: {metrics.get('optical_similarity', 0):.2f}
- Consistência RF: {metrics.get('rf_consistency', 0):.2f}
- Integridade do Selo: {metrics.get('tamper_evidence', 0):.2f}

Timestamp: {event.get('timestamp', 'N/A')}

Emita um laudo forense completo com:
1. Conclusão objetiva (AUTÊNTICO / SUSPEITO / FRAUDADO)
2. Fundamentação técnica detalhada
3. Amparo legal (LGPD, CPC, Marco Civil)
4. Recomendação de conduta
5. Assinatura criptográfica simulada (SHA-256)"""


def setup_model_and_tokenizer():
    """Configura o modelo e tokenizer com quantização 4-bit."""
    print(f"📦 Carregando modelo: {MODEL_NAME}")
    
    # Configuração de quantização 4-bit (QLoRA)
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
    )
    
    # Carrega modelo
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
    )
    
    # Prepara modelo para k-bit training
    model = prepare_model_for_kbit_training(model)
    
    # Carrega tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME,
        trust_remote_code=True,
    )
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
    
    return model, tokenizer


def setup_lora(model):
    """Configura os adaptadores LoRA."""
    print("🔧 Configurando adaptadores LoRA...")
    
    lora_config = LoraConfig(
        r=16,  # rank
        lora_alpha=32,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )
    
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    
    return model


def tokenize_function(examples, tokenizer):
    """Tokeniza os exemplos para treinamento."""
    # Formata como instruction tuning
    texts = [
        f"<|im_start|>user\n{inp}<|im_end|>\n<|im_start|>assistant\n{out}<|im_end|>"
        for inp, out in zip(examples["input"], examples["output"])
    ]
    
    tokenized = tokenizer(
        texts,
        truncation=True,
        max_length=MAX_SEQ_LENGTH,
        padding="max_length",
        return_tensors=None,
    )
    
    return tokenized


def main():
    parser = argparse.ArgumentParser(description="Fine-tuning Magistrado Themis")
    parser.add_argument("--epochs", type=int, default=3, help="Número de épocas")
    parser.add_argument("--batch_size", type=int, default=4, help="Batch size")
    parser.add_argument("--learning_rate", type=float, default=2e-4, help="Learning rate")
    parser.add_argument("--output_dir", type=str, default=OUTPUT_DIR, help="Diretório de saída")
    args = parser.parse_args()
    
    print(f"\n🧠 Magistrado Themis — Fine-Tuning (GATE 2)")
    print(f"📅 Iniciado em: {datetime.now().isoformat()}")
    print(f"⚙️  Configurações: epochs={args.epochs}, batch_size={args.batch_size}, lr={args.learning_rate}\n")
    
    # 1. Carrega dataset
    print("📂 Carregando dataset forense...")
    dataset = load_dataset(DATASET_PATH)
    print(f"✅ Dataset carregado: {len(dataset)} exemplos")
    
    # 2. Setup modelo e tokenizer
    model, tokenizer = setup_model_and_tokenizer()
    
    # 3. Configura LoRA
    model = setup_lora(model)
    
    # 4. Tokeniza dataset
    print("🔤 Tokenizando dataset...")
    tokenized_dataset = dataset.map(
        lambda x: tokenize_function(x, tokenizer),
        batched=True,
        remove_columns=dataset.column_names,
    )
    
    # 5. Configura treinamento
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=1,
        learning_rate=args.learning_rate,
        fp16=True,
        logging_steps=10,
        save_steps=50,
        save_total_limit=2,
        optim="paged_adamw_32bit",
        lr_scheduler_type="cosine",
        warmup_ratio=0.03,
        report_to="none",  # Desativa wandb/mlflow
    )
    
    # 6. Inicia treinamento
    print("\n🚀 Iniciando fine-tuning...")
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        tokenizer=tokenizer,
    )
    
    trainer.train()
    
    # 7. Salva modelo
    print(f"\n💾 Salvando modelo em: {args.output_dir}")
    trainer.save_model(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)
    
    print(f"\n✅ Fine-tuning concluído em: {datetime.now().isoformat()}")
    print(f"📊 Modelo salvo em: {args.output_dir}")


if __name__ == "__main__":
    main()
