"""
DIONYSUS Super-Base Training (Phase 2)
Trains merged super-base model (Theia-8B + Phase 1 LoRA) for 9000 steps
"""

import os
import sys
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import load_dataset

# Configuration
MERGED_MODEL_PATH = "N:/OCEANS/oceans_training/merged_superbase/dionysus"
OUTPUT_DIR = "N:/OCEANS/oceans_training/outputs_dionysus_superbase"
DATASET_PATH = "N:/OCEANS/oceans_training/datasets/dionysus_meme_intelligence/training_corpus_final.jsonl"

# Training hyperparameters - FULL TRAINING
MAX_STEPS = 9000  # Full training for proper base model
BATCH_SIZE = 2  # Reduced from 4 due to full fine-tuning (not LoRA)
GRADIENT_ACCUMULATION = 8  # Increased to maintain effective batch size of 16
LEARNING_RATE = 2e-5  # Lower LR for fine-tuning merged model
WARMUP_STEPS = 500
LOGGING_STEPS = 50
SAVE_STEPS = 1000

print("=" * 70, flush=True)
print("DIONYSUS SUPER-BASE TRAINING (PHASE 2)", flush=True)
print("=" * 70, flush=True)
print(f"Merged model: {MERGED_MODEL_PATH}", flush=True)
print(f"Output: {OUTPUT_DIR}", flush=True)
print(f"Max steps: {MAX_STEPS} (FULL TRAINING)", flush=True)
print(f"GPU: CUDA:0 (RTX 5090)", flush=True)
print("=" * 70, flush=True)

# Set CUDA device
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

# Load merged model
print("\nLoading merged super-base model...", flush=True)
model = AutoModelForCausalLM.from_pretrained(
    MERGED_MODEL_PATH,
    torch_dtype=torch.bfloat16,  # Use BF16 instead of FP16 for gradient checkpointing compatibility
    device_map="auto",
    trust_remote_code=True
)

# Load tokenizer
print("Loading tokenizer...", flush=True)
tokenizer = AutoTokenizer.from_pretrained(
    MERGED_MODEL_PATH,
    trust_remote_code=True
)

# Set padding token if not set
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
    model.config.pad_token_id = model.config.eos_token_id

# Enable gradient checkpointing for memory efficiency
print("Enabling gradient checkpointing...", flush=True)
model.gradient_checkpointing_enable()

# Freeze some layers to reduce memory usage (train only top layers)
print("Freezing bottom 50% of model layers...", flush=True)
total_layers = len(model.model.layers)
freeze_layers = total_layers // 2
for i in range(freeze_layers):
    for param in model.model.layers[i].parameters():
        param.requires_grad = False

# Count trainable parameters
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
all_params = sum(p.numel() for p in model.parameters())
print(f"trainable params: {trainable_params} || all params: {all_params} || trainable%: {100 * trainable_params / all_params:.4f}", flush=True)

# Load dataset
print("\nLoading training dataset...", flush=True)
dataset = load_dataset('json', data_files=DATASET_PATH, split='train')
print(f"Dataset size: {len(dataset)} examples", flush=True)

# Tokenize function
def tokenize_function(examples):
    return tokenizer(
        examples['text'],
        truncation=True,
        max_length=512,
        padding='max_length'
    )

print("Tokenizing dataset...", flush=True)
tokenized_dataset = dataset.map(
    tokenize_function,
    batched=True,
    remove_columns=dataset.column_names
)

# Data collator
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)

# Training arguments
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    max_steps=MAX_STEPS,
    per_device_train_batch_size=BATCH_SIZE,
    gradient_accumulation_steps=GRADIENT_ACCUMULATION,
    learning_rate=LEARNING_RATE,
    warmup_steps=WARMUP_STEPS,
    logging_steps=LOGGING_STEPS,
    save_steps=SAVE_STEPS,
    save_total_limit=3,
    fp16=False,  # Disabled FP16
    bf16=True,   # Use BF16 instead for gradient checkpointing compatibility
    optim="adamw_torch",
    report_to="none",
    logging_dir=f"{OUTPUT_DIR}/logs",
    load_best_model_at_end=False,
    gradient_checkpointing=True,
    ddp_find_unused_parameters=False
)

# Create trainer
print("\nInitializing trainer...", flush=True)
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    data_collator=data_collator
)

# Train
print("\n" + "=" * 70, flush=True)
print("STARTING DIONYSUS SUPER-BASE TRAINING", flush=True)
print("=" * 70, flush=True)
print(f"Total steps: {MAX_STEPS}", flush=True)
print(f"Effective batch size: {BATCH_SIZE * GRADIENT_ACCUMULATION}", flush=True)
print(f"Checkpoints every {SAVE_STEPS} steps", flush=True)
print("=" * 70 + "\n", flush=True)

try:
    trainer.train()

    print("\n" + "=" * 70, flush=True)
    print("TRAINING COMPLETE - SAVING FINAL MODEL", flush=True)
    print("=" * 70, flush=True)

    # Save final model
    trainer.save_model(f"{OUTPUT_DIR}/final_model")
    tokenizer.save_pretrained(f"{OUTPUT_DIR}/final_model")

    print(f"\nFinal model saved to: {OUTPUT_DIR}/final_model", flush=True)
    print("\nSUCCESS: DIONYSUS super-base training complete!", flush=True)

except Exception as e:
    print(f"\nERROR during training: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)
