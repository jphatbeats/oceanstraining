#!/usr/bin/env python3
# generate_runpod.py — Phase 15 donor sample generation (local models, 8-bit)

import os, sys, json, time, math, argparse, random
from pathlib import Path

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)

# ---------- SETTINGS ----------
# Local donor paths already on disk:
DONOR_PATHS = {
    "finma":        "/workspace/models/finma-7b",       # ChanceFocus/finma-7b-full
    "finance_llm":  "/workspace/models/finance-llm",    # AdaptLLM/finance-chat
    "nemotron":     "/workspace/models/nemotron-8b",    # nvidia/Nemotron-8B-Instruct
    # Keep BERTs out of generation; they are analyzers only.
    # "finbert":    "/workspace/models/finbert",
    # "cryptobert": "/workspace/models/cryptobert",
}

# Where to write JSONL samples
OUT_DIR = Path("/workspace/oceanstraining/out")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Minimal prompts per entity to bootstrap; you can tune these in the repo later.
ENTITY_PROMPTS = {
    "ARIA": [
        "Summarize the current crypto market structure in one tight paragraph, then list three likely catalysts.",
        "Explain a precise, step-by-step plan to scan social + orderflow for early momentum on mid-cap alts.",
        "Draft the exact questions you'd ask a trader before approving a position."
    ],
    "DIONYSUS": [
        "Roast a weak meme coin launch while secretly pointing to one signal that could flip it bullish.",
        "Give a hype thread outline (5 bullets) for a meme coin that actually has solid token mechanics.",
        "List three on-chain tricks for catching whale rotations early, with cautions."
    ],
    "SAGE": [
        "Summarize macro in 6 sentences max: rates, liquidity, risk appetite, and how that spills into crypto.",
        "If CPI surprises high tomorrow, lay out two scenarios for BTC and SOL with specific levels.",
        "Explain how ETF flows and funding rates combine into a weekly bias."
    ],
    "HYDRA": [
        "Write a TMZ-style leak on a protocol's rumored partnership, but keep it grounded in signals we can verify.",
        "Draft a 6-step social sweep that converts raw chaos into a tradable watchlist.",
        "Explain how to separate bot noise from real momentum in trending hashtags."
    ],
}

# Default sample targets (small smoke test). Use --profile=50k to expand later.
SAMPLE_TARGETS_PRESETS = {
    "quick": {
        "ARIA":      {"finma": 50,   "finance_llm": 50},
        "DIONYSUS":  {"nemotron": 75},
        "SAGE":      {"finma": 50},
        "HYDRA":     {"nemotron": 75},
    },
    # Matches your "Option 2 – 50K exact" pattern but with only causal donors
    # (we split SAGE/HYDRA across finma/nemotron to keep it simple & fast).
    "50k": {
        "ARIA":      {"finance_llm": 6000},  # finma already complete (6000 samples)
        "DIONYSUS":  {"nemotron": 15000},
        "SAGE":      {"finma": 6000, "nemotron": 6000},
        "HYDRA":     {"nemotron": 11000},
    }
}

# Generation hyperparameters (safe defaults for 8-bit on A6000)
GEN_KW = dict(
    max_new_tokens=256,       # Max tokens to generate (prevents infinite loops)
    do_sample=True,
    temperature=0.8,
    top_p=0.95,
    top_k=50,
    repetition_penalty=1.05,
    eos_token_id=None,        # Will be set per-model
)

# ---------- UTIL ----------

def log_box(title: str):
    line = "=" * (len(title) + 2)
    print(f"\n+{line}+\n| {title} |\n+{line}+\n")

def set_seeds(seed: int = 42):
    random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

def resolve_pad_ids(tok):
    # Get pad token ID without modifying tokenizer (avoids .to() calls)
    pad_id = tok.pad_token_id
    if pad_id is None:
        # Use eos_token_id as fallback (don't assign to tok.pad_token)
        pad_id = tok.eos_token_id if tok.eos_token_id is not None else 0
    return pad_id

def load_causal_model(local_path: str):
    if not Path(local_path).exists():
        raise FileNotFoundError(f"Model folder not found: {local_path}")

    tok = AutoTokenizer.from_pretrained(
        local_path,
        use_fast=True,
        trust_remote_code=True,
    )
    pad_id = resolve_pad_ids(tok)

    # Try 8-bit first, fall back to fp16 if model config conflicts with quantization
    try:
        print("   Attempting 8-bit quantization...")
        model = AutoModelForCausalLM.from_pretrained(
            local_path,
            load_in_8bit=True,
            device_map="auto",
            trust_remote_code=True,
        )
        print("   ✅ 8-bit quantization successful")
    except Exception as e:
        if ".to` is not supported" in str(e):
            print(f"   ⚠️ 8-bit failed (model config conflict), falling back to fp16...")
            model = AutoModelForCausalLM.from_pretrained(
                local_path,
                torch_dtype=torch.float16,
                device_map="auto",
                trust_remote_code=True,
            )
            print("   ✅ fp16 fallback successful")
        else:
            raise

    # Skip resize for quantized models - causes .to() errors
    # Tokenizers should already match model vocab size

    return tok, model, pad_id

def generate_samples(entity: str, donor_key: str, n_samples: int):
    model_dir = DONOR_PATHS[donor_key]
    print(f"\n> {entity}: loading donor '{donor_key}' from {model_dir}")
    tok, model, pad_id = load_causal_model(model_dir)
    model.eval()

    prompts = ENTITY_PROMPTS[entity]
    out_path = OUT_DIR / f"{entity.lower()}_{donor_key}.jsonl"
    written = 0

    # Check if model is quantized (8-bit models don't need input device movement)
    is_quantized = getattr(model, "is_quantized", False) or hasattr(model, "hf_quantizer")

    with out_path.open("a", encoding="utf-8") as f:
        for i in range(n_samples):
            prompt = random.choice(prompts)

            # Simple chat-ish prefix if the donor expects instructions
            if hasattr(tok, "apply_chat_template") and tok.apply_chat_template is not None:
                messages = [
                    {"role": "system", "content": f"You are {entity}, an expert agent in a crypto-AI trading collective."},
                    {"role": "user", "content": prompt},
                ]
                # Don't use return_tensors - tokenize the formatted text instead
                formatted = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
                input_ids = tok(formatted, return_tensors="pt").input_ids
            else:
                input_ids = tok(prompt, return_tensors="pt").input_ids

            # For fp16 models, move inputs to same device as model
            if not is_quantized:
                input_ids = input_ids.to(model.device)

            # Set proper EOS token to prevent infinite generation
            gen_kwargs = GEN_KW.copy()
            gen_kwargs['eos_token_id'] = tok.eos_token_id

            with torch.no_grad():
                outputs = model.generate(
                    input_ids,
                    pad_token_id=pad_id,
                    **gen_kwargs,
                )
            text = tok.decode(outputs[0], skip_special_tokens=True)

            record = {
                "entity": entity,
                "donor": donor_key,
                "prompt": prompt,
                "response": text.strip(),
                "ts": int(time.time()),
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            written += 1

            if written % 25 == 0:
                print(f"  ... {written}/{n_samples} for {entity}:{donor_key}")

    print(f"Wrote {written} samples to {out_path}")
    return out_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--profile",
        choices=["quick", "50k"],
        default=os.environ.get("OCEANS_PROFILE", "quick"),
        help="Sample size profile (quick=small smoke test, 50k=full run)."
    )
    args = parser.parse_args()

    set_seeds(42)

    title = f"PHASE 15: RUNPOD A6000 GENERATION  -  profile={args.profile}"
    log_box(title)
    print("8-bit quantization - safetensors-only - local donors\n")

    targets = SAMPLE_TARGETS_PRESETS[args.profile]
    total = sum(sum(d.values()) for d in targets.values())
    print(f"Planned total samples: ~{total}\n")

    for entity, donor_counts in targets.items():
        print("#" * 80)
        print(f"# ENTITY: {entity}")
        print("# DONORS:", ", ".join(donor_counts.keys()))
        print("#" * 80)

        for donor_key, n in donor_counts.items():
            if donor_key not in DONOR_PATHS:
                print(f"Skipping unknown donor '{donor_key}'")
                continue
            try:
                generate_samples(entity, donor_key, n)
            except Exception as e:
                print(f"ERROR {entity}:{donor_key} failed - {e}")

    print("\nDone. JSONL outputs are in:", str(OUT_DIR))


if __name__ == "__main__":
    main()
