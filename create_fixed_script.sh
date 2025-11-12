#!/bin/bash
# Create the FIXED training script directly
cat > /workspace/train_dionysus_trading_runpod_FIXED.py << 'ENDOFFILE'
"""
DIONYSUS TRADING BRAIN TRAINING SCRIPT - RUNPOD A6000 (FIXED)
======================================================
Trains DIONYSUS trading brain on phi3:mini with 4-bit QLoRA.
Fixed tokenization issue.
"""

import os
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    BitsAndBytesConfig
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from transformers import DataCollatorForLanguageModeling
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
BASE_MODEL = "microsoft/Phi-3-mini-4k-instruct"
ENTITY_NAME = "DIONYSUS_TRADING"
DATASET_PATH = "/workspace/datasets/DIONYSUS_trading_brain_ENHANCED.jsonl"
OUTPUT_DIR = "/workspace/output/dionysus_trading_adapter"
CACHE_DIR = "/workspace/.cache"

# Training hyperparameters
TRAINING_CONFIG = {
    "num_train_epochs": 1,
    "max_steps": 2500,
    "per_device_train_batch_size": 4,
    "gradient_accumulation_steps": 4,
    "learning_rate": 2e-5,
    "warmup_steps": 50,
    "logging_steps": 10,
    "save_steps": 250,
    "save_total_limit": 3,
    "fp16": True,
    "optim": "paged_adamw_8bit",
    "lr_scheduler_type": "cosine",
    "max_grad_norm": 1.0,
}

# LoRA configuration
LORA_CONFIG = {
    "r": 16,
    "lora_alpha": 32,
    "target_modules": ["qkv_proj", "o_proj", "gate_up_proj", "down_proj"],
    "lora_dropout": 0.05,
    "bias": "none",
    "task_type": "CAUSAL_LM"
}

# 4-bit quantization config
QUANT_CONFIG = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True
)

def main():
    logger.info("=" * 70)
    logger.info(f"TRAINING {ENTITY_NAME} ON RUNPOD A6000")
    logger.info("=" * 70)

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)

    # Load dataset
    logger.info(f"\n[1/6] Loading dataset: {DATASET_PATH}")
    dataset = load_dataset("json", data_files=DATASET_PATH, split="train", cache_dir=CACHE_DIR)
    logger.info(f"  Loaded {len(dataset):,} samples")

    # Load tokenizer
    logger.info(f"\n[2/6] Loading tokenizer: {BASE_MODEL}")
    tokenizer = AutoTokenizer.from_pretrained(
        BASE_MODEL,
        cache_dir=CACHE_DIR,
        trust_remote_code=True
    )
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    # Tokenize dataset - FIXED VERSION (robust clean)
    logger.info("\n[3/6] Tokenizing dataset...")
    def tokenize_function(examples):
        # Ensure every text entry is a string
        texts = []
        for t in examples["text"]:
            if isinstance(t, dict):
                # Handle structured fields like {"role": "user", "content": "..."}
                t = t.get("content", "")
            elif t is None:
                t = ""
            texts.append(str(t))

        return tokenizer(
            texts,
            truncation=True,
            max_length=2048,
            padding="max_length"
        )

    tokenized_dataset = dataset.map(
        tokenize_function,
        batched=True,
        remove_columns=dataset.column_names,
        desc="Tokenizing"
    )
    logger.info(f"  Tokenized {len(tokenized_dataset):,} samples")

    # Load base model in 4-bit
    logger.info(f"\n[4/6] Loading base model (4-bit): {BASE_MODEL}")
    logger.info("  This may take 2-3 minutes...")
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        quantization_config=QUANT_CONFIG,
        device_map="auto",
        cache_dir=CACHE_DIR,
        trust_remote_code=True
    )
    logger.info("  Base model loaded successfully!")

    # Prepare model for training
    logger.info("\n[5/6] Preparing model for k-bit training...")
    model = prepare_model_for_kbit_training(model)

    # Add LoRA adapters
    logger.info(f"  Adding LoRA adapters (r={LORA_CONFIG['r']}, alpha={LORA_CONFIG['lora_alpha']})...")
    lora_config = LoraConfig(**LORA_CONFIG)
    model = get_peft_model(model, lora_config)

    # Print trainable parameters
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total_params = sum(p.numel() for p in model.parameters())
    logger.info(f"  Trainable params: {trainable_params:,} ({trainable_params/total_params*100:.2f}%)")
    logger.info(f"  Total params: {total_params:,}")

    # Training arguments
    logger.info("\n[6/6] Setting up training...")
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        **TRAINING_CONFIG
    )

    # Data collator (like working scripts use)
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )

    # Create trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        data_collator=data_collator
    )

    # Start training
    logger.info("\n" + "=" * 70)
    logger.info(f"STARTING {ENTITY_NAME} TRAINING")
    logger.info("=" * 70)
    logger.info(f"Dataset: {len(tokenized_dataset):,} samples")
    logger.info(f"Steps: {TRAINING_CONFIG['max_steps']:,}")
    logger.info(f"Estimated time: ~2-3 hours")
    logger.info("=" * 70)
    logger.info("\nTraining started...\n")

    # Train!
    trainer.train()

    # Save final model
    logger.info("\n" + "=" * 70)
    logger.info(f"{ENTITY_NAME} TRAINING COMPLETE!")
    logger.info("=" * 70)
    logger.info(f"\nSaving final adapter to {OUTPUT_DIR}...")
    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)

    # Get adapter size
    adapter_file = os.path.join(OUTPUT_DIR, "adapter_model.safetensors")
    if os.path.exists(adapter_file):
        size_mb = os.path.getsize(adapter_file) / (1024 * 1024)
        logger.info(f"  Adapter saved: {size_mb:.1f} MB")

    logger.info("\n" + "=" * 70)
    logger.info("SUCCESS!")
    logger.info("=" * 70)
    logger.info(f"\nOutput directory: {OUTPUT_DIR}")
    logger.info("\nDONE! Trade execution intelligence UPGRADED!")

if __name__ == "__main__":
    main()
ENDOFFILE

echo "Training script created successfully!"
ls -lh /workspace/train_dionysus_trading_runpod_FIXED.py
