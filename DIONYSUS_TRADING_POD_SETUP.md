# DIONYSUS-TRADING POD SETUP GUIDE
**Pod**: DIONYSUS-TRADING (Pod 3)
**Model**: microsoft/Phi-3-mini-4k-instruct
**Dataset**: DIONYSUS_trading_brain_ENHANCED.jsonl (20 MB, 28,464 samples)
**Purpose**: Fast execution decision-making brain with complete Pump.fun knowledge

---

## ✅ ENVIRONMENT VERIFIED

Your RunPod environment is READY:
```
Python 3.11.10               ✅
PyTorch 2.5.1+cu121          ✅
CUDA 12.1                    ✅
transformers 4.40.0          ✅
peft 0.17.1                  ✅
bitsandbytes 0.48.2          ✅
accelerate 1.11.0            ✅
datasets 4.4.1               ✅
```

NO PACKAGE INSTALLATION NEEDED - Environment is perfect! 🎯

---

## 📦 STEP 1: UPLOAD FILES TO POD

You need to upload 2 files from your local machine to the RunPod:

### File 1: Training Script
**Local Path**: `N:/OCEANS/oceans_training/train_dionysus_trading_runpod.py`
**Upload To**: `/workspace/train_dionysus_trading_runpod.py`

### File 2: Training Dataset
**Local Path**: `N:/OCEANS/oceans_training/data/final_training/DIONYSUS_trading_brain_ENHANCED.jsonl`
**Upload To**: `/workspace/datasets/DIONYSUS_trading_brain_ENHANCED.jsonl`

⚠️ **CRITICAL**: Use the ENHANCED version (20 MB, 28,464 samples)
❌ **NOT**: DIONYSUS_trading_brain.jsonl (17 MB, old version)

---

## 📋 STEP 2: VERIFY UPLOADS

Run these commands on the RunPod to verify files are uploaded correctly:

```bash
# Check training script is present
ls -lh /workspace/train_dionysus_trading_runpod.py

# Check dataset is present
ls -lh /workspace/datasets/DIONYSUS_trading_brain_ENHANCED.jsonl

# Verify dataset size (should be ~20 MB)
du -h /workspace/datasets/DIONYSUS_trading_brain_ENHANCED.jsonl

# Count samples (should be 28,464 lines)
wc -l /workspace/datasets/DIONYSUS_trading_brain_ENHANCED.jsonl
```

Expected Output:
```
-rw-r--r-- 1 root root 7.0K Nov 11 XX:XX /workspace/train_dionysus_trading_runpod.py
-rw-r--r-- 1 root root 20M  Nov 11 XX:XX /workspace/datasets/DIONYSUS_trading_brain_ENHANCED.jsonl
20M     /workspace/datasets/DIONYSUS_trading_brain_ENHANCED.jsonl
28464 /workspace/datasets/DIONYSUS_trading_brain_ENHANCED.jsonl
```

---

## 🚀 STEP 3: START TRAINING

Once files are uploaded and verified, start training:

```bash
cd /workspace

# Start training in background with logging
nohup python train_dionysus_trading_runpod.py > training.log 2>&1 &

# Note the process ID that's displayed
echo $! > training.pid
```

---

## 📊 STEP 4: MONITOR TRAINING PROGRESS

### View Real-Time Progress
```bash
# Watch training log (press Ctrl+C to exit)
tail -f /workspace/training.log
```

### Check Current Status
```bash
# View last 50 lines of log
tail -n 50 /workspace/training.log

# Check if training process is still running
ps aux | grep train_dionysus_trading_runpod.py

# Check GPU utilization
nvidia-smi
```

### What You Should See

**Initial Output** (first few minutes):
```
=================================================================
DIONYSUS TRADING BRAIN TRAINING - RUNPOD
=================================================================
Base Model: microsoft/Phi-3-mini-4k-instruct
Dataset: /workspace/datasets/DIONYSUS_trading_brain_ENHANCED.jsonl
Output: /workspace/output/dionysus_trading_adapter

Loading base model...
Loading dataset...
Dataset loaded: 28,464 samples

Starting training...
Step 1/2500 | Loss: 2.45 | Time: 3.2s
Step 2/2500 | Loss: 2.38 | Time: 3.1s
Step 3/2500 | Loss: 2.31 | Time: 3.0s
...
```

**Mid-Training** (after ~1 hour):
```
Step 500/2500 | Loss: 0.85 | Time: 2.8s
Step 1000/2500 | Loss: 0.42 | Time: 2.7s
Step 1500/2500 | Loss: 0.31 | Time: 2.7s
...
```

**Final Output** (after ~2-3 hours):
```
Step 2500/2500 | Loss: 0.18 | Time: 2.7s

Training complete!
Model saved to: /workspace/output/dionysus_trading_adapter

Adapter files:
  - adapter_model.safetensors (~25 MB)
  - adapter_config.json
  - tokenizer_config.json
  - tokenizer files

DIONYSUS TRADING BRAIN READY FOR EXECUTION! ⚡
```

---

## ⏱️ EXPECTED TIMELINE

| Stage | Duration | Cumulative |
|-------|----------|------------|
| Model Download | 5-10 min | 10 min |
| Dataset Loading | 1-2 min | 12 min |
| Training (2,500 steps) | 2-3 hours | ~3 hours |
| **TOTAL** | **~3 hours** | **~3 hours** |

**Note**: DIONYSUS-TRADING finishes FASTER than other pods because:
- Smaller model (Phi-3-mini vs Qwen3-30B)
- Smaller dataset (28,464 vs 197,479+ samples)
- Fewer training steps (2,500 vs 9,900)

---

## 💾 STEP 5: DOWNLOAD TRAINED ADAPTER

Once training completes (you'll see "Training complete!" in the log):

```bash
# Verify adapter was created
ls -lh /workspace/output/dionysus_trading_adapter/

# Check adapter size (should be ~25 MB)
du -sh /workspace/output/dionysus_trading_adapter/
```

Expected files:
```
/workspace/output/dionysus_trading_adapter/
├── adapter_model.safetensors    (~25 MB)
├── adapter_config.json
├── tokenizer_config.json
├── tokenizer.json
├── special_tokens_map.json
└── tokenizer_model
```

### Download Adapter to Local Machine

**Using RunPod Web Interface**:
1. Navigate to `/workspace/output/dionysus_trading_adapter/`
2. Select all files
3. Click "Download" button
4. Save to: `N:/OCEANS/oceans_training/output/dionysus_trading_adapter/`

**Using SCP/SFTP** (if you have SSH access):
```bash
# From your local Windows machine
scp -r root@<POD_IP>:/workspace/output/dionysus_trading_adapter N:/OCEANS/oceans_training/output/
```

---

## 🛑 STEP 6: STOP POD (IMPORTANT!)

**CRITICAL**: Once adapter is downloaded, IMMEDIATELY stop the pod to avoid charges!

RunPod charges $0.49/hour - every hour the pod runs costs money.

### Stop Pod
1. Go to RunPod dashboard
2. Find your DIONYSUS-TRADING pod
3. Click "Stop" or "Terminate"
4. Verify pod is stopped (status should show "Stopped")

**Cost Check**:
- 3 hours training + 1 hour buffer = 4 hours
- 4 hours × $0.49/hour = **~$2.00 total** ✅

---

## ⚠️ TROUBLESHOOTING

### Error: "CUDA out of memory"
**Solution**: The Phi-3-mini model should fit easily in 48GB. If you see this error:
```bash
# Check what's using VRAM
nvidia-smi

# Kill any other processes using GPU
pkill -f jupyter
pkill -f python

# Restart training
nohup python train_dionysus_trading_runpod.py > training.log 2>&1 &
```

### Error: "Dataset file not found"
**Solution**: Verify file path and name:
```bash
# Check exact filename (case-sensitive!)
ls -la /workspace/datasets/

# Make sure it's DIONYSUS_trading_brain_ENHANCED.jsonl
# NOT DIONYSUS_trading_brain.jsonl (old version)
```

### Training Seems Stuck
**Solution**: Check if process is still running:
```bash
# View last 20 lines of log
tail -n 20 /workspace/training.log

# Check process status
ps aux | grep train_dionysus

# Check GPU activity
nvidia-smi
```

If GPU utilization is 0% and no new log entries for 10+ minutes:
```bash
# Kill stuck process
pkill -f train_dionysus_trading_runpod.py

# Restart training
nohup python train_dionysus_trading_runpod.py > training.log 2>&1 &
```

### Loss Not Decreasing
**Expected behavior**:
- Initial loss: 2.0-3.0
- After 500 steps: 0.8-1.2
- After 1000 steps: 0.4-0.7
- Final loss: 0.15-0.30

If loss stays above 2.0 after 500 steps, check:
```bash
# Verify dataset is ENHANCED version
wc -l /workspace/datasets/DIONYSUS_trading_brain_ENHANCED.jsonl
# Should show: 28464

# Check first few samples
head -n 3 /workspace/datasets/DIONYSUS_trading_brain_ENHANCED.jsonl
# Should show JSON with Pump.fun knowledge
```

---

## ✅ SUCCESS CHECKLIST

Before stopping the pod, verify:

- [ ] Training completed (2,500/2,500 steps)
- [ ] Final loss < 0.30
- [ ] Adapter files created in `/workspace/output/dionysus_trading_adapter/`
- [ ] `adapter_model.safetensors` is ~25 MB
- [ ] Adapter downloaded to local machine
- [ ] Downloaded files verified (adapter_config.json, tokenizer files present)
- [ ] Pod STOPPED (no more charges!)

---

## 🎯 NEXT STEPS

After DIONYSUS-TRADING training completes:

**Pod 1: ARIA** (Intelligence Coordinator)
- Dataset: ARIA_final_training.jsonl (109 MB, 197,479 samples)
- Training time: ~7 hours

**Pod 2: DIONYSUS-RESEARCH** (Meme Analysis)
- Dataset: DIONYSUS_final_training.jsonl (113 MB, 201,215 samples)
- Training time: ~7 hours

**Pod 4: SAGE** (News Intelligence)
- Dataset: SAGE_final_training.jsonl (107 MB, 194,479 samples)
- Training time: ~7 hours

**Pod 5: HYDRA** (Social Intelligence)
- Dataset: HYDRA_final_training.jsonl (110 MB, 201,215 samples)
- Training time: ~7 hours

---

## 📋 QUICK COMMAND REFERENCE

```bash
# Upload verification
ls -lh /workspace/train_dionysus_trading_runpod.py
ls -lh /workspace/datasets/DIONYSUS_trading_brain_ENHANCED.jsonl
wc -l /workspace/datasets/DIONYSUS_trading_brain_ENHANCED.jsonl

# Start training
cd /workspace
nohup python train_dionysus_trading_runpod.py > training.log 2>&1 &

# Monitor progress
tail -f /workspace/training.log
nvidia-smi

# Check completion
ls -lh /workspace/output/dionysus_trading_adapter/
du -sh /workspace/output/dionysus_trading_adapter/

# Stop pod after download (RunPod dashboard)
```

---

**STATUS**: READY TO START TRAINING ✅

Upload the 2 files, verify, and start training! The Ocean's fastest execution brain is about to awaken! 🌊⚡
