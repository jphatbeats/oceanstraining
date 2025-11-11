"""
DIONYSUS TRAINING SCRIPT - RUNPOD A6000
========================================
Trains DIONYSUS entity on Qwen3-30B base with 4-bit QLoRA.

Dataset: DIONYSUS_final_training.jsonl (201,215 samples)
Base Model: Qwen/Qwen3-30B-A3B-Instruct-2507
Hardware: A6000 48GB VRAM
Training Time: ~6.9 hours
Output: dionysus_adapter.safetensors (~50-60MB)

Usage:
    python train_dionysus_runpod.py
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
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURATION
# ============================================================================

# Model
BASE_MODEL = "Qwen/Qwen3-30B-A3B-Instruct-2507"
ENTITY_NAME = "DIONYSUS"

# Paths (adjust for RunPod environment)
DATASET_PATH = "/workspace/datasets/DIONYSUS_final_training.jsonl"
OUTPUT_DIR = "/workspace/output/dionysus_adapter"
CACHE_DIR = "/workspace/.cache"

# Training hyperparameters
TRAINING_CONFIG = {
    "num_train_epochs": 1,
    "max_steps": 10000,
    "per_device_train_batch_size": 4,
    "gradient_accumulation_steps": 4,  # Effective batch size = 16
    "learning_rate": 1e-5,
    "warmup_steps": 100,
    "logging_steps": 10,
    "save_steps": 500,
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
    "target_modules": ["q_proj", "v_proj", "k_proj", "o_proj"],
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

# ============================================================================
# MAIN TRAINING
# ============================================================================

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

    # Tokenize dataset
    logger.info("\n[3/6] Tokenizing dataset...")
    def tokenize_function(examples):
        return tokenizer(
            examples["text"],
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
    logger.info("  This may take 5-10 minutes...")
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

    # Create trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        tokenizer=tokenizer
    )

    # Start training
    logger.info("\n" + "=" * 70)
    logger.info(f"STARTING {ENTITY_NAME} TRAINING")
    logger.info("=" * 70)
    logger.info(f"Dataset: {len(tokenized_dataset):,} samples")
    logger.info(f"Steps: {TRAINING_CONFIG['max_steps']:,}")
    logger.info(f"Batch size: {TRAINING_CONFIG['per_device_train_batch_size']}")
    logger.info(f"Gradient accumulation: {TRAINING_CONFIG['gradient_accumulation_steps']}")
    logger.info(f"Effective batch size: {TRAINING_CONFIG['per_device_train_batch_size'] * TRAINING_CONFIG['gradient_accumulation_steps']}")
    logger.info(f"Learning rate: {TRAINING_CONFIG['learning_rate']}")
    logger.info(f"Estimated time: ~6.9 hours")
    logger.info("=" * 70)
    logger.info("\nTraining started... (monitor with 'tail -f' on the log file)\n")

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
    logger.info("Files:")
    logger.info("  - adapter_model.safetensors (LoRA weights)")
    logger.info("  - adapter_config.json (LoRA configuration)")
    logger.info("  - tokenizer files")
    logger.info("\nNext: Download these files and deploy to local DIONYSUS server!")
    logger.info("\nDONE! 🌊⚡")

if __name__ == "__main__":
    main()
