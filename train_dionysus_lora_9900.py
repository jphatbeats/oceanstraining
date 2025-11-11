"""
DIONYSUS LoRA Training - FULL 9900 STEPS
Trains LoRA adapter on Qwen3-30B-A3B-Instruct-2507 base model (MoE: 30.5B total, 3.3B activated)
Fast LoRA training: ~2.5 sec/step = ~6.9 hours total
"""

import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
os.environ['HF_HOME'] = 'N:/OCEANS/oceans_training/.cache/huggingface'
os.environ['BITSANDBYTES_NOWELCOME'] = '1'
os.environ['DISABLE_BITSANDBYTES'] = '1'

import torch
from pathlib import Path
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, TaskType

print("=" * 70)
print("DIONYSUS LORA TRAINING - FULL 9900 STEPS")
print("=" * 70)

# Check GPU
if torch.cuda.is_available():
    print(f"\nGPU Available: {torch.cuda.get_device_name(0)}")
    print(f"CUDA Version: {torch.version.cuda}")
else:
    print("\nERROR: No GPU available!")
    exit(1)

# Paths
BASE_MODEL = "N:/OCEANS/oceans_training/merged_superbase/dionysus"  # Local merged Qwen3 model
CORPUS_FILE = "N:/OCEANS/oceans_training/data/super_mix/DIONYSUS_super_mix.jsonl"
OUTPUT_DIR = "N:/OCEANS/oceans_training/outputs_dionysus_lora_9900"

MODEL_PATH = BASE_MODEL
print(f"\nUsing base model: {BASE_MODEL}")

# LoRA config
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

# Training config - 9900 STEPS
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    max_steps=9900,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=1e-5,
    warmup_steps=500,
    logging_steps=50,
    save_steps=1000,
    save_total_limit=3,
    fp16=False,
    bf16=True,
    optim="adamw_torch",
    lr_scheduler_type="cosine",
    report_to="none",
    remove_unused_columns=False
)

print("\n" + "=" * 70)
print("LOADING MODEL & TOKENIZER...")
print("=" * 70)

# Load tokenizer
print("\n[1/4] Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token

# Load model
print("\n[2/4] Loading base model...")
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.bfloat16,
    device_map={"": 0},
    trust_remote_code=True,
    low_cpu_mem_usage=True
)

# Apply LoRA
print("\n[3/4] Applying LoRA adapters...")
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# Load dataset
print("\n[4/4] Loading training corpus...")
dataset = load_dataset('json', data_files=CORPUS_FILE, split='train')
print(f"Loaded {len(dataset)} samples")

# Tokenize
def tokenize_function(examples):
    return tokenizer(
        examples["text"],
        truncation=True,
        max_length=512,
        padding="max_length"
    )

print("\nTokenizing dataset...")
tokenized_dataset = dataset.map(tokenize_function, batched=True, remove_columns=dataset.column_names)

# Data collator
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)

# Trainer
print("\n" + "=" * 70)
print("INITIALIZING TRAINER...")
print("=" * 70)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    data_collator=data_collator
)

# Train!
print("\n" + "=" * 70)
print("STARTING DIONYSUS LORA TRAINING - 9900 STEPS")
print("=" * 70)
print(f"\nMax steps: {training_args.max_steps}")
print(f"Batch size: {training_args.per_device_train_batch_size}")
print(f"Gradient accumulation: {training_args.gradient_accumulation_steps}")
print(f"Effective batch size: {training_args.per_device_train_batch_size * training_args.gradient_accumulation_steps}")
print(f"Learning rate: {training_args.learning_rate}")
print(f"\nEstimated time: ~6.9 hours (2.5 sec/step)")
print("=" * 70)

try:
    trainer.train()

    print("\n" + "=" * 70)
    print("TRAINING COMPLETE!")
    print("=" * 70)

    # Save final model
    final_dir = Path(OUTPUT_DIR) / "final_model"
    trainer.save_model(str(final_dir))
    tokenizer.save_pretrained(str(final_dir))
    print(f"\nFinal model saved: {final_dir}")

except KeyboardInterrupt:
    print("\n\nTraining interrupted by user!")
    print("Saving checkpoint...")
    trainer.save_model(str(Path(OUTPUT_DIR) / "interrupted_checkpoint"))

except Exception as e:
    print(f"\n\nERROR during training: {e}")
    import traceback
    traceback.print_exc()

print("\nTraining session ended.")
