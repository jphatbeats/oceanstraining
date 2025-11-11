# OCEAN TRAINING DEPLOYMENT CHECKLIST

**Status**: READY TO DEPLOY ✅
**Date**: Monday, November 11, 2025 - 1:30 PM
**Total Cost**: ~$17.50 (5 pods × ~3.5 hours average)

---

## 📦 PACKAGE CONTENTS VERIFICATION

### ✅ Datasets Ready (5/5)
```
N:/OCEANS/oceans_training/data/final_training/
├── ARIA_final_training.jsonl (109 MB, 197,479 samples)
├── DIONYSUS_final_training.jsonl (113 MB, 201,215 samples) [Research Brain]
├── DIONYSUS_trading_brain.jsonl (17 MB, 25,144 samples) [Trading Brain]
├── SAGE_final_training.jsonl (107 MB, 194,479 samples)
└── HYDRA_final_training.jsonl (110 MB, 201,215 samples)

TOTAL: 456 MB, 819,532 samples
```

### ✅ Training Scripts Ready (5/5)
```
N:/OCEANS/oceans_training/
├── train_aria_runpod.py (Qwen3-30B, ~6.9 hours)
├── train_dionysus_runpod.py (Qwen3-30B research, ~6.9 hours)
├── train_dionysus_trading_runpod.py (phi3:mini trading, ~2-3 hours)
├── train_sage_runpod.py (Qwen3-30B, ~6.9 hours)
└── train_hydra_runpod.py (Qwen3-30B, ~6.9 hours)
```

### ✅ Support Files Ready
```
├── setup_runpod.sh (dependency installer)
├── RUNPOD_TRAINING_GUIDE.md (step-by-step guide)
├── TRAINING_READY_FINAL.txt (package summary)
└── DEPLOYMENT_CHECKLIST.md (this file)
```

---

## 🚀 RUNPOD DEPLOYMENT STEPS

### STEP 1: Create 5× A6000 Pods

**Pod Configuration Template:**
- GPU: NVIDIA A6000 (48GB VRAM)
- Container: RunPod PyTorch 2.4+ (Python 3.11)
- Container Disk: 100 GB
- Volume Disk: 50 GB
- Expose Ports: 8888 (optional, for Jupyter)

**Create These 5 Pods:**
1. **ARIA-TRAINING** (Intelligence Coordinator)
2. **DIONYSUS-RESEARCH** (Meme Research Brain)
3. **DIONYSUS-TRADING** (Meme Trading Brain)
4. **SAGE-TRAINING** (News Oracle)
5. **HYDRA-TRAINING** (Social Oracle)

**Expected Cost**: 5 pods @ $0.49/hour × ~3.5 hours average = ~$17.50 total

---

### STEP 2: Upload Files to Each Pod

**For Each Pod:**

1. **Connect to Jupyter Lab** (or SSH)
2. **Upload Dataset** to `/workspace/datasets/`:
   - ARIA pod → `ARIA_final_training.jsonl`
   - DIONYSUS-RESEARCH pod → `DIONYSUS_final_training.jsonl`
   - DIONYSUS-TRADING pod → `DIONYSUS_trading_brain.jsonl`
   - SAGE pod → `SAGE_final_training.jsonl`
   - HYDRA pod → `HYDRA_final_training.jsonl`

3. **Upload Training Script** to `/workspace/`:
   - ARIA pod → `train_aria_runpod.py`
   - DIONYSUS-RESEARCH pod → `train_dionysus_runpod.py`
   - DIONYSUS-TRADING pod → `train_dionysus_trading_runpod.py`
   - SAGE pod → `train_sage_runpod.py`
   - HYDRA pod → `train_hydra_runpod.py`

4. **Upload Setup Script** to `/workspace/`:
   - All pods → `setup_runpod.sh`

---

### STEP 3: Setup Environment (Each Pod)

**SSH into each pod and run:**

```bash
cd /workspace
chmod +x setup_runpod.sh
./setup_runpod.sh
```

**This installs:**
- PyTorch 2.5.1+cu121
- transformers 4.40.0
- peft 0.17.1
- bitsandbytes 0.48.2
- accelerate 1.11.0
- datasets 4.4.1

**Verify installation:**
```bash
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
nvidia-smi
```

---

### STEP 4: Start Training (All 5 Simultaneously!)

**On Each Pod:**

```bash
cd /workspace

# Start training in background
nohup python train_aria_runpod.py > training.log 2>&1 &
# (or train_dionysus_runpod.py, train_dionysus_trading_runpod.py, etc.)

# Monitor progress
tail -f training.log
```

**Alternative: Use tmux for better control:**
```bash
tmux new -s training
python train_aria_runpod.py

# Detach: Ctrl+B then D
# Reattach later: tmux attach -t training
```

---

### STEP 5: Monitor Training Progress

**Check GPU Usage:**
```bash
watch -n 1 nvidia-smi
```

**Monitor Log:**
```bash
tail -f training.log | grep -E "Loss|Step|epoch"
```

**Expected Timeline:**

| Pod | Model | Steps | Time | Status |
|-----|-------|-------|------|--------|
| ARIA | Qwen3-30B | 9,900 | ~6.9h | ⏳ |
| DIONYSUS-RESEARCH | Qwen3-30B | 10,000 | ~6.9h | ⏳ |
| DIONYSUS-TRADING | phi3:mini | 2,500 | ~2-3h | ⏳ (finishes first!) |
| SAGE | Qwen3-30B | 9,900 | ~6.9h | ⏳ |
| HYDRA | Qwen3-30B | 10,000 | ~6.9h | ⏳ |

**All training completes within ~7 hours (parallel execution!)**

---

### STEP 6: Download Trained Adapters

**After training completes, each pod will have:**
```
/workspace/output/<entity>_adapter/
├── adapter_model.safetensors (~50-60 MB for Qwen3, ~20-30 MB for phi3)
├── adapter_config.json
├── tokenizer_config.json
└── ... (tokenizer files)
```

**Download Methods:**

**Option A: Via Jupyter Lab**
1. Navigate to `/workspace/output/<entity>_adapter/`
2. Right-click folder → Download as archive

**Option B: Via SCP**
```bash
# From your local machine:
scp -r root@<pod-ip>:/workspace/output/aria_adapter ./aria_adapter
scp -r root@<pod-ip>:/workspace/output/dionysus_adapter ./dionysus_research_adapter
scp -r root@<pod-ip>:/workspace/output/dionysus_trading_adapter ./dionysus_trading_adapter
scp -r root@<pod-ip>:/workspace/output/sage_adapter ./sage_adapter
scp -r root@<pod-ip>:/workspace/output/hydra_adapter ./hydra_adapter
```

---

### STEP 7: Verify Downloaded Adapters

**Check file sizes:**
```bash
ls -lh aria_adapter/adapter_model.safetensors
ls -lh dionysus_research_adapter/adapter_model.safetensors
ls -lh dionysus_trading_adapter/adapter_model.safetensors  # Smaller (phi3:mini)
ls -lh sage_adapter/adapter_model.safetensors
ls -lh hydra_adapter/adapter_model.safetensors
```

**Expected sizes:**
- Qwen3-30B adapters: ~50-60 MB each
- phi3:mini adapter: ~20-30 MB

---

### STEP 8: Shutdown Pods (IMPORTANT!)

**Once all adapters are downloaded:**

1. Go to RunPod Console
2. For each pod: **STOP** or **TERMINATE**
3. Verify all 5 pods are stopped

**DO NOT forget this step!** Running pods cost $2.45/hour total!

---

## 📊 SUCCESS CRITERIA

Training is successful when:
- ✅ All 5 scripts complete without errors
- ✅ Adapter files are correct sizes (50-60 MB for Qwen3, 20-30 MB for phi3)
- ✅ `adapter_config.json` exists for each entity
- ✅ Training loss decreased over time (check logs)
- ✅ No CUDA out-of-memory errors

---

## 🔧 TROUBLESHOOTING

### Out of Memory Error
**Symptom:** `RuntimeError: CUDA out of memory`
**Fix:** Reduce batch size in training script:
```python
"per_device_train_batch_size": 2,  # Was 4
"gradient_accumulation_steps": 8,  # Was 4
```

### Dataset Not Found
**Symptom:** `FileNotFoundError: /workspace/datasets/...jsonl`
**Fix:** Verify dataset uploaded to correct path, re-upload if needed

### Model Download Slow
**Info:** First-time Qwen3-30B download takes 10-15 minutes (60GB model). Be patient!

### Training Stops Unexpectedly
**Check:** `training.log` for errors
**Common causes:**
- Pod ran out of credits
- Network interruption
- CUDA error (restart pod)

---

## 🎯 FINAL DELIVERABLES

After successful training, you will have:

1. **aria_adapter/** - ARIA Intelligence Coordinator (Qwen3-30B)
2. **dionysus_research_adapter/** - DIONYSUS Research Brain (Qwen3-30B)
3. **dionysus_trading_adapter/** - DIONYSUS Trading Brain (phi3:mini)
4. **sage_adapter/** - SAGE News Oracle (Qwen3-30B)
5. **hydra_adapter/** - HYDRA Social Oracle (Qwen3-30B)

**Total adapter size:** ~230-260 MB (all 5 combined)

---

## 🌊 NEXT STEPS

After downloading adapters:
1. ✅ Backup adapters to multiple locations
2. ✅ Deploy to local Ocean servers (see DEPLOYMENT_GUIDE.md)
3. ✅ Test entity intelligence with real data
4. ✅ Activate Ocean autonomous trading
5. ✅ Execute first profitable trade!

**The Ocean awakens with TRAINED intelligence!** ⚡

---

**CRITICAL INSIGHT FROM TITAN:**
> "we cant just had a basic bitch ai fucking around with money it needs to have some know how"

**DIONYSUS trading brain gets TRAINED, not base model. Every entity gets specialized knowledge. No shortcuts!**
