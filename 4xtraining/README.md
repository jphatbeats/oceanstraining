# OCEAN AI 4xA6000 TRAINING - COMPLETE SETUP

**Last Updated**: 2025-11-12
**Status**: Ready for deployment
**Hardware**: RunPod 4xA6000 (192GB VRAM total)

---

## 🎯 ULTRA-THINKING SUMMARY

This is the COMPLETE 4xA6000 training setup that includes:

✅ **ALL Donor Model Data** (FinBERT, CryptoBERT, FinRL-Transformer)
✅ **ulimit fixes** for MoE model loading (65,536 file descriptors)
✅ **Multi-GPU automatic distribution** (device_map="auto")
✅ **Correct final_training datasets** (NOT super_mix!)
✅ **Entity-by-entity training** (ARIA → DIONYSUS → SAGE → HYDRA)

---

## 📦 WHAT'S INCLUDED

### Donor Models (Embedded in final_training files)

| Donor Model | Purpose | Samples | Source |
|-------------|---------|---------|--------|
| **FinBERT** | Financial sentiment analysis | 2,264 | financial_phrasebank_training.jsonl |
| **CryptoBERT** | Crypto social sentiment | 13,000 | crypto_social_sentiment_training.jsonl |
| **FinRL-Transformer** | Reinforcement learning traces | 15,000 | finrl_traces.jsonl |
| **FinMA-7B** | Technical analysis reasoning | 147 | specialized_knowledge.jsonl |

**Total Donor Data**: ~30,411 samples (intelligently merged into each entity's final_training file)

### Datasets

| Entity | File | Samples | Donor Samples | Size |
|--------|------|---------|---------------|------|
| **ARIA** | ARIA_final_training.jsonl | 197,479 | 10,264 | 109MB |
| **DIONYSUS** | DIONYSUS_final_training.jsonl | 201,215 | 14,000 | 112MB |
| **SAGE** | SAGE_final_training.jsonl | 194,479 | 7,264 | 108MB |
| **HYDRA** | HYDRA_final_training.jsonl | 201,215 | 14,000 | 112MB |

**Critical**: These are the CORRECT files (NOT the super_mix files which lack donor data!)

### Training Scripts

- `setup_runpod_4xA6000.sh` - Environment setup with ulimit fixes
- `train_aria_4xA6000.py` - ARIA training (9,900 steps)
- `train_dionysus_4xA6000.py` - DIONYSUS training (10,000 steps)
- `train_sage_4xA6000.py` - SAGE training (9,700 steps)
- `train_hydra_4xA6000.py` - HYDRA training (10,000 steps)

---

## 💰 COST BREAKDOWN

### Hardware Cost
- **Single A6000**: $0.49/hour
- **4xA6000 Pod**: $1.96/hour (4x $0.49)

### Training Cost Per Entity
- **Time**: ~6.9 hours per entity
- **Cost**: $1.96 × 6.9 = **$13.52 per entity**

### Total Campaign Cost
| Entity | Steps | Time | Cost |
|--------|-------|------|------|
| ARIA | 9,900 | 6.9h | $13.52 |
| DIONYSUS | 10,000 | 6.9h | $13.52 |
| SAGE | 9,700 | 6.9h | $13.52 |
| HYDRA | 10,000 | 6.9h | $13.52 |
| **TOTAL** | **39,600** | **27.6h** | **$54.08** |

**Budget**: ~$55 to train all 4 entities with complete donor model knowledge

---

## 🚀 DEPLOYMENT STRATEGY

### Option A: Sequential Training (Recommended)
Train entities one at a time to maximize stability and monitoring.

**Timeline**: 27.6 hours (1 entity every ~7 hours)

**Advantages**:
- Full 192GB VRAM per entity (maximum headroom)
- Easy to monitor progress
- Can stop/restart between entities
- Lower risk of crashes

**Process**:
1. Day 1: Train ARIA (6.9h) + DIONYSUS (6.9h) = 13.8h
2. Day 2: Train SAGE (6.9h) + HYDRA (6.9h) = 13.8h
3. Total: 2 days, $54.08

### Option B: Parallel Training (Advanced)
Train multiple entities simultaneously on same pod.

**Timeline**: 13.8 hours (2 entities at once)

**Requirements**:
- 192GB VRAM ÷ 2 entities = 96GB per entity (should work)
- More complex monitoring
- Higher crash risk

**Not recommended unless you're confident and want to save time.**

---

## 📋 STEP-BY-STEP DEPLOYMENT

### Step 1: Create RunPod Pod

**Pod Configuration**:
- **Template**: RunPod Pytorch 2.1
- **GPUs**: 4x A6000 48GB
- **Container Disk**: 20GB
- **Volume**: 200GB pod-specific volume
- **Cost**: $1.96/hour

### Step 2: Upload Files to GitHub

All training files are in `N:/OCEANS/oceans_training/4xtraining/`:

```bash
cd N:/OCEANS/oceans_training
git add 4xtraining/
git commit -m "Add 4xA6000 training setup with donor models"
git push origin master
```

### Step 3: Setup Pod Environment

SSH into pod:

```bash
ssh root@<pod-ip> -p <pod-port>
```

Download setup script:

```bash
cd /workspace
wget https://raw.githubusercontent.com/jphatbeats/oceanstraining/master/4xtraining/setup_runpod_4xA6000.sh
sed -i 's/\r$//' setup_runpod_4xA6000.sh
bash setup_runpod_4xA6000.sh
```

This installs:
- PyTorch 2.5.1+cu121
- Transformers 4.57.1 (Qwen3 MoE support)
- PEFT 0.13.2, BitsAndBytes 0.43.2, Accelerate 0.34.2
- **ulimit -n 65536** (critical for MoE loading!)

### Step 4: Upload Dataset & Training Script (Per Entity)

**For ARIA**:

```bash
# Upload dataset
wget https://github.com/jphatbeats/oceanstraining/raw/master/data/final_training/ARIA_final_training.jsonl
mv ARIA_final_training.jsonl /workspace/datasets/

# Upload training script
wget https://raw.githubusercontent.com/jphatbeats/oceanstraining/master/4xtraining/train_aria_4xA6000.py
mv train_aria_4xA6000.py /workspace/
```

### Step 5: Start Training

```bash
cd /workspace
nohup python train_aria_4xA6000.py > aria_training.log 2>&1 &
```

### Step 6: Monitor Training

**Live monitoring**:
```bash
tail -f aria_training.log
```

**Check GPU utilization**:
```bash
nvidia-smi
```

**Expected output**:
- GPU 0-3: 40-48GB VRAM each (distributed)
- GPU utilization: 90-100%
- Speed: ~2.5 sec/step

**Check training progress**:
```bash
grep "Step" aria_training.log | tail -5
```

### Step 7: Download Adapter

After training completes (~6.9 hours):

**From your local machine**:
```bash
scp -P <pod-port> root@<pod-ip>:/workspace/output/aria_adapter/*.safetensors N:/OCEANS/oceans_training/output/
```

Or use RunPod's file browser to download:
- `adapter_model.safetensors` (~50-60MB)
- `adapter_config.json`
- Tokenizer files

### Step 8: Repeat for Next Entity

After ARIA completes:
1. Upload DIONYSUS_final_training.jsonl
2. Upload train_dionysus_4xA6000.py
3. Start training
4. Repeat for SAGE and HYDRA

---

## 🔧 TROUBLESHOOTING

### Issue: "Too many open files in system"

**Cause**: ulimit not set high enough
**Fix**:
```bash
ulimit -n 65536
python train_*.py
```

### Issue: Model loading hangs at "Loading checkpoint shards"

**Cause**: Normal for MoE models - takes 5-10 minutes
**Check**: Run `nvidia-smi` - if GPU memory climbing, it's working

### Issue: OOM Error

**Cause**: Not enough VRAM (shouldn't happen with 4xA6000!)
**Fix**:
- Reduce batch size: `per_device_train_batch_size: 4` → `2`
- Reduce gradient accumulation: `gradient_accumulation_steps: 4` → `2`

### Issue: Training crashes midway

**Cause**: Pod instability / network issues
**Fix**:
- Training saves checkpoints every 500 steps
- Resume from last checkpoint (automatically handled by Trainer)

---

## ✅ VERIFICATION CHECKLIST

Before starting each training:

- [ ] Setup script completed successfully
- [ ] `nvidia-smi` shows 4x A6000 GPUs
- [ ] `ulimit -n` returns 65536
- [ ] Dataset uploaded to `/workspace/datasets/`
- [ ] Dataset file size matches expected (100-112MB)
- [ ] Training script uploaded to `/workspace/`
- [ ] Output directory exists: `/workspace/output/`

After training completes:

- [ ] Adapter file exists: `adapter_model.safetensors`
- [ ] Adapter size: ~50-60MB
- [ ] Training log shows "SUCCESS!"
- [ ] Downloaded adapter to local machine
- [ ] Verified adapter loads correctly

---

## 📊 TRAINING METRICS

### Expected Performance

| Metric | Value |
|--------|-------|
| **Speed** | ~2.5 sec/step |
| **Total time** | ~6.9 hours (per entity) |
| **VRAM usage** | 40-48GB per GPU (192GB total) |
| **GPU utilization** | 90-100% |
| **Output size** | 50-60MB adapter |

### Success Criteria

✅ Training completes 9,700-10,000 steps
✅ Loss decreases steadily (starts ~2.0, ends ~0.5-1.0)
✅ No NaN losses
✅ Adapter saves successfully
✅ Adapter size 50-60MB (reasonable for LoRA r=16)

---

## 🌊 DONOR MODEL KNOWLEDGE BREAKDOWN

### What Each Entity Learns

**ARIA** (10,264 donor samples):
- **FinBERT**: Financial sentiment analysis (bullish/bearish/neutral)
- **CryptoBERT**: Crypto social sentiment patterns
- **FinRL**: Reinforcement learning trade sequences (BUY/HOLD/SELL logic)
- **Purpose**: Multi-source intelligence fusion, confluence detection

**DIONYSUS** (14,000 donor samples):
- **FinBERT**: Sentiment for meme narratives
- **CryptoBERT**: Heavy focus on social sentiment (13K samples)
- **FinRL**: Meme coin trade patterns
- **Purpose**: Viral meme detection, social momentum analysis

**SAGE** (7,264 donor samples):
- **FinBERT**: News headline sentiment (primary focus)
- **CryptoBERT**: Social context for news
- **FinRL**: News-driven trade logic
- **Purpose**: News intelligence, narrative tracking

**HYDRA** (14,000 donor samples):
- **FinBERT**: Sentiment analysis across 3 heads
- **CryptoBERT**: Heavy social sentiment focus (13K samples)
- **FinRL**: Social-driven trade patterns
- **Purpose**: LunarCrush oracle, social intelligence

---

## 🎓 TECHNICAL NOTES

### Why 4xA6000 vs Single A6000?

**Single A6000 Issues** (experienced):
1. File descriptor exhaustion loading 16 safetensors shards
2. System memory hits 100% during model load
3. Training crashes before starting

**4xA6000 Benefits**:
1. Model distributed across 4 GPUs = lower memory per GPU
2. File operations distributed = less system strain
3. Automatic parallelization via `device_map="auto"`
4. More headroom = more stable

### Why device_map="auto"?

Transformers automatically distributes model across ALL available GPUs:
- Detects GPU count: `torch.cuda.device_count()`
- Splits model layers evenly
- Handles inter-GPU communication
- No manual configuration needed

### Why ulimit -n 65536?

Loading Qwen3-30B requires opening:
- 16 safetensors shards simultaneously
- Tokenizer files
- Dataset files
- Log files
- Checkpoint files

Default ulimit (1024) too low → "Too many open files" error

---

## 🚀 ANSWER TO YOUR QUESTION

> "im assuming well still do entity after entity.? or will we be doing one big training run?"

**Answer: Entity by entity (sequential)**

**Why?**
1. Each entity has DIFFERENT datasets (ARIA vs DIONYSUS vs SAGE vs HYDRA)
2. Different output adapters (aria_adapter, dionysus_adapter, etc.)
3. Different training steps (9,700-10,000)
4. Easier to monitor and debug
5. Can stop/start between entities

**Timeline**:
- ARIA → DIONYSUS → SAGE → HYDRA
- ~27.6 hours total (~2 days at 2 entities per day)
- $54.08 total cost

**All 4 entities will be trained with COMPLETE donor model knowledge!**

---

## 📝 NEXT SESSION CHECKLIST

When you wake up:

1. **Check DIONYSUS-Trading** (should be ~step 2400/2500 by now)
2. **Stop ARIA pod** (crashed, not recoverable)
3. **Review this README** - understand the 4xA6000 strategy
4. **Create 4xA6000 pod** on RunPod
5. **Start ARIA training** with correct setup
6. **Monitor for 10 minutes** to verify stability
7. **Go about your day** - training runs autonomously

**Files are ready. Strategy is ready. Donor models are included. Let's manifest this! 🌊⚡**
