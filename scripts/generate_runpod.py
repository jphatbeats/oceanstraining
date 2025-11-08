"""
PHASE 15 - RunPod A6000 Generation
Optimized for 48GB VRAM - 8-bit quantization for large models
"""

import os
import json
import torch
from pathlib import Path
from tqdm import tqdm
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    AutoModelForCausalLM,
    pipeline
)

# RunPod paths
OUTPUT_PATH = Path("/workspace/donordata")
MODEL_PATH = Path("/workspace/models")

# Local model mappings
MODELS = {
    "finbert": MODEL_PATH / "finbert",
    "cryptobert": MODEL_PATH / "cryptobert",
    "finma": MODEL_PATH / "finma-7b",
    "finance_llm": MODEL_PATH / "finance-llm",
    "nemotron": MODEL_PATH / "nemotron-8b"
}

# Import prompts
from entity_prompts_runpod import get_prompts_for_entity, get_sample_target

class DonorSampleGenerator:
    """Generate training samples from a donor model"""

    def __init__(self, donor_name, model_type="llama"):
        self.donor_name = donor_name
        self.model_type = model_type
        self.model = None
        self.tokenizer = None
        self.pipeline = None

    def load_model(self):
        """Load the donor model - Optimized for A6000 48GB"""
        print(f"\n[{self.donor_name.upper()}] Loading model...")

        model_path = str(MODELS[self.donor_name])

        if self.model_type == "bert":
            # BERT models (FinBERT, CryptoBERT) - ~2GB each
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModelForSequenceClassification.from_pretrained(
                model_path,
                device_map="auto"
            )
            self.pipeline = pipeline(
                "sentiment-analysis",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0
            )
            print(f"   ✅ BERT model loaded on GPU")

        elif self.model_type == "llama":
            # LLaMA models - Use 8-bit for 51GB models on 48GB GPU
            from transformers import BitsAndBytesConfig

            quantization_config = BitsAndBytesConfig(
                load_in_8bit=True,
                llm_int8_threshold=6.0
            )

            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_path,
                device_map="auto",
                torch_dtype=torch.float16,
                quantization_config=quantization_config
                # use_safetensors auto-detects - models are already in safetensors format
            )
            print(f"   ✅ LLaMA model loaded in 8-bit (~25GB VRAM)")

    def generate_sample_bert(self, prompt):
        """Generate sample using BERT model"""
        result = self.pipeline(prompt[:512])[0]

        sentiment_map = {
            "LABEL_0": "bearish",
            "LABEL_1": "neutral",
            "LABEL_2": "bullish"
        }

        sentiment = sentiment_map.get(result['label'], "neutral")
        score = result['score']

        response = f"""Sentiment Analysis:
- Sentiment: {sentiment}
- Confidence: {score:.2f}
- Assessment: {'Strong signal' if score > 0.8 else 'Moderate signal' if score > 0.6 else 'Weak signal'}
- Recommendation: {'Act on this' if score > 0.75 else 'Monitor' if score > 0.5 else 'Low priority'}
"""
        return response

    def generate_sample_llama(self, prompt):
        """Generate sample using LLaMA model"""
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=512,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = response[len(prompt):].strip()
        return response

    def generate_samples(self, entity_name, num_samples):
        """Generate N samples for a specific entity"""
        print(f"\n{'='*80}")
        print(f"Generating {num_samples} samples for {entity_name} using {self.donor_name.upper()}")
        print(f"{'='*80}\n")

        base_prompts = get_prompts_for_entity(entity_name)
        if not base_prompts:
            print(f"   ⚠️ No prompts found for {entity_name}")
            return []

        samples = []

        with tqdm(total=num_samples, desc=f"{entity_name}/{self.donor_name}") as pbar:
            while len(samples) < num_samples:
                for base_prompt in base_prompts:
                    if len(samples) >= num_samples:
                        break

                    if self.model_type == "bert":
                        response = self.generate_sample_bert(base_prompt)
                    elif self.model_type == "llama":
                        response = self.generate_sample_llama(base_prompt)
                    else:
                        response = None

                    if response:
                        sample = {
                            "messages": [
                                {"role": "system", "content": f"You are {entity_name}, an AI entity in the Ocean trading system."},
                                {"role": "user", "content": base_prompt},
                                {"role": "assistant", "content": response}
                            ],
                            "source": self.donor_name,
                            "entity": entity_name
                        }
                        samples.append(sample)
                        pbar.update(1)

        return samples

    def save_samples(self, entity_name, samples):
        """Save generated samples to .jsonl file"""
        output_dir = OUTPUT_PATH / entity_name
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / f"{self.donor_name}_samples.jsonl"

        print(f"\n💾 Saving {len(samples)} samples to {output_file}")

        with open(output_file, 'w', encoding='utf-8') as f:
            for sample in samples:
                f.write(json.dumps(sample) + '\n')

        size_mb = output_file.stat().st_size / (1024 * 1024)
        print(f"   ✅ Saved {size_mb:.2f} MB")

    def cleanup(self):
        """Free up GPU memory"""
        if self.model is not None:
            del self.model
            del self.tokenizer
            if self.pipeline is not None:
                del self.pipeline
            torch.cuda.empty_cache()
            print(f"   ✅ {self.donor_name.upper()} unloaded from GPU")

def main():
    """Main generation pipeline for RunPod A6000"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║            PHASE 15: RUNPOD A6000 GENERATION                 ║
║                                                              ║
║  48GB VRAM - 8-bit quantization, maximum speed!             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")

    # Entity → Donor mapping
    entity_donors = {
        "ARIA": [
            {"name": "finma", "type": "llama"},
            {"name": "finance_llm", "type": "llama"}
        ],
        "DIONYSUS": [
            {"name": "cryptobert", "type": "bert"},
            {"name": "finbert", "type": "bert"},
            {"name": "nemotron", "type": "llama"}  # Local model
        ],
        "SAGE": [
            {"name": "finma", "type": "llama"},
            {"name": "finbert", "type": "bert"}
        ],
        "HYDRA": [
            {"name": "cryptobert", "type": "bert"},
            {"name": "finbert", "type": "bert"}
        ]
    }

    # Generate for each entity
    for entity, donors in entity_donors.items():
        print(f"\n{'#'*80}")
        print(f"# ENTITY: {entity}")
        print(f"# DONORS: {', '.join([d['name'] for d in donors])}")
        print(f"{'#'*80}")

        for config in donors:
            donor_name = config['name']
            model_type = config['type']
            target_samples = get_sample_target(entity, donor_name)

            generator = DonorSampleGenerator(donor_name, model_type)
            generator.load_model()
            samples = generator.generate_samples(entity, target_samples)
            generator.save_samples(entity, samples)
            generator.cleanup()

    print(f"\n{'='*80}")
    print("🌊 RUNPOD GENERATION COMPLETE")
    print(f"{'='*80}")
    print(f"\nOutput location: /workspace/donordata/")
    print(f"\nNext: Download results to local machine")

if __name__ == "__main__":
    main()
