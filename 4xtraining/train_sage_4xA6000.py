"""
SAGE TRAINING SCRIPT - RUNPOD 4xA6000
======================================
Trains SAGE entity on Qwen3-30B base with 4-bit QLoRA.

Dataset: SAGE_final_training.jsonl (194,479 samples)
  - News intelligence (651 RSS feeds)
  - Market narratives (30%)
  - Episodes & system knowledge (20%)
  - **DONOR MODELS (7,264 samples):**
    - FinBERT sentiment (2,264 samples)
    - CryptoBERT social (subsampled)
    - FinRL reinforcement traces (subsampled)

Base Model: Qwen/Qwen3-30B-A3B-Instruct-2507
Hardware: 4xA6000 192GB VRAM (distributed automatically)
Training Time: ~6.9 hours
Output: sage_adapter.safetensors (~50-60MB)

Usage:
    python train_sage_4xA6000.py
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

# ============================================================================
# CONFIGURATION
# ============================================================================

# Model
BASE_MODEL = "Qwen/Qwen3-30B-A3B-Instruct-2507"
ENTITY_NAME = "SAGE"

# Paths (RunPod 4xA6000 environment)
DATASET_PATH = "/workspace/datasets/SAGE_final_training.jsonl"
OUTPUT_DIR = "/workspace/output/sage_adapter"
CACHE_DIR = "/workspace/.cache"

# Training hyperparameters
TRAINING_CONFIG = {
    "num_train_epochs": 1,
    "max_steps": 9700,
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
    logger.info(f"TRAINING {ENTITY_NAME} ON RUNPOD 4xA6000")
    logger.info("=" * 70)

    # Check GPU count
    gpu_count = torch.cuda.device_count()
    logger.info(f"\n🎮 Detected {gpu_count} GPUs:")
    for i in range(gpu_count):
        logger.info(f"  GPU {i}: {torch.cuda.get_device_name(i)}")
    logger.info("")

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)

    # Load dataset
    logger.info(f"\n[1/6] Loading dataset: {DATASET_PATH}")
    dataset = load_dataset("json", data_files=DATASET_PATH, split="train", cache_dir=CACHE_DIR)
    logger.info(f"  Loaded {len(dataset):,} samples")
    logger.info(f"  ✓ Includes 7,264 donor model samples (FinBERT, CryptoBERT, FinRL)")

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

    # Load base model in 4-bit (device_map="auto" distributes across ALL GPUs)
    logger.info(f"\n[4/6] Loading base model (4-bit): {BASE_MODEL}")
    logger.info(f"  Distributing across {gpu_count} GPUs automatically...")
    logger.info("  This may take 5-10 minutes...")
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        quantization_config=QUANT_CONFIG,
        device_map="auto",  # Automatic multi-GPU distribution
        cache_dir=CACHE_DIR,
        trust_remote_code=True
    )
    logger.info("  Base model loaded successfully!")
    logger.info(f"  ✓ Model distributed across {gpu_count} GPUs")

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
    logger.info(f"Dataset: {len(tokenized_dataset):,} samples (including donor models)")
    logger.info(f"Steps: {TRAINING_CONFIG['max_steps']:,}")
    logger.info(f"Batch size: {TRAINING_CONFIG['per_device_train_batch_size']}")
    logger.info(f"Gradient accumulation: {TRAINING_CONFIG['gradient_accumulation_steps']}")
    logger.info(f"Effective batch size: {TRAINING_CONFIG['per_device_train_batch_size'] * TRAINING_CONFIG['gradient_accumulation_steps']}")
    logger.info(f"Learning rate: {TRAINING_CONFIG['learning_rate']}")
    logger.info(f"GPUs: {gpu_count}x A6000 (192GB total VRAM)")
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
    logger.info("\nNext: Download these files and deploy to local SAGE server!")
    logger.info("\nDONE! 🌊⚡")

if __name__ == "__main__":
    main()
