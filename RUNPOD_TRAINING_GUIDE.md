# 🚀 RUNPOD PARALLEL TRAINING GUIDE

**Complete guide to train all 4 Ocean entities simultaneously on RunPod A6000 GPUs.**

---

## 📋 WHAT WE'RE TRAINING

| Entity | Dataset | Samples | Output |
|--------|---------|---------|--------|
| **ARIA** | ARIA_final_training.jsonl | 197,479 | aria_adapter.safetensors |
| **DIONYSUS** | DIONYSUS_final_training.jsonl | 201,215 | dionysus_adapter.safetensors |
| **SAGE** | SAGE_final_training.jsonl | 194,479 | sage_adapter.safetensors |
| **HYDRA** | HYDRA_final_training.jsonl | 201,215 | hydra_adapter.safetensors |

**Total**: 794,388 samples → 4× LoRA adapters (~50-60MB each)

---

## ⚙️ TRAINING CONFIGURATION

**Base Model**: Qwen/Qwen3-30B-A3B-Instruct-2507
**Method**: 4-bit QLoRA (r=16, alpha=32, dropout=0.05)
**Hardware**: A6000 48GB VRAM (one per entity)

**Training Parameters**:
- Steps: ~9,900-10,000 per entity
- Batch size: 4
- Gradient accumulation: 4 (effective batch = 16)
- Learning rate: 1e-5
- Warmup: 100 steps
- Time: ~6.9 hours per entity
- Cost: ~$3.50 per pod = **$14 total**

---

## 🔧 STEP 1: PREPARE RUNPOD PODS (4× Pods)

### 1.1 Create Pod #1 (ARIA)

1. Go to https://www.runpod.io/console/pods
2. Click "Deploy"
3. Select **NVIDIA A6000 (48GB VRAM)**
4. Container Image: `runpod/pytorch:2.1.0-py3.10-cuda12.1.0-devel-ubuntu22.04`
5. Container Disk: **100 GB**
6. Volume Disk: **50 GB** (persistent storage)
7. Expose HTTP Ports: **8888** (for Jupyter if needed)
8. Pod Name: **ARIA-TRAINING**
9. Click **Deploy**

### 1.2 Repeat for Pods #2, #3, #4

- Pod #2: **DIONYSUS-TRAINING**
- Pod #3: **SAGE-TRAINING**
- Pod #4: **HYDRA-TRAINING**

**Cost**: 4× A6000 @ $0.49/hour = $1.96/hour

---

## 📦 STEP 2: UPLOAD DATASETS

### Option A: Via RunPod File Manager (Easiest)

For each pod:
1. Click "Connect" → "Connect to Jupyter Lab"
2. Upload the corresponding dataset:
   - Pod 1 (ARIA): Upload `ARIA_final_training.jsonl`
   - Pod 2 (DIONYSUS): Upload `DIONYSUS_final_training.jsonl`
   - Pod 3 (SAGE): Upload `SAGE_final_training.jsonl`
   - Pod 4 (HYDRA): Upload `HYDRA_final_training.jsonl`
3. Move to `/workspace/datasets/` directory

### Option B: Via SCP/SFTP

```bash
# Get SSH connection info from RunPod pod page
# Example for ARIA pod:
scp ARIA_final_training.jsonl root@<pod-ip>:/workspace/datasets/
```

### Option C: Via Git (If Using RunPod Git)

```bash
# On each pod:
cd /workspace
git clone <your-repo>
cp oceanstraining/out/*.jsonl /workspace/datasets/
```

---

## 🔧 STEP 3: SETUP ENVIRONMENT (Each Pod)

### 3.1 SSH into Pod

Click "Connect" → "Start Web Terminal" or use SSH

### 3.2 Install Dependencies

```bash
# Install required packages
pip install -U transformers accelerate peft bitsandbytes datasets

# Verify CUDA
nvidia-smi
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

### 3.3 Upload Training Script

Upload the corresponding script to each pod:
- Pod 1 (ARIA): `train_aria_runpod.py`
- Pod 2 (DIONYSUS): `train_dionysus_runpod.py`
- Pod 3 (SAGE): `train_sage_runpod.py`
- Pod 4 (HYDRA): `train_hydra_runpod.py`

Save to `/workspace/train.py` on each pod

---

## 🚀 STEP 4: START TRAINING (All 4 Simultaneously!)

### On Each Pod:

```bash
cd /workspace

# Start training in background with logging
nohup python train.py > training.log 2>&1 &

# Monitor progress
tail -f training.log
```

**Alternative** (run in tmux session):
```bash
tmux new -s training
python train.py

# Detach: Ctrl+B, then D
# Reattach: tmux attach -t training
```

---

## 📊 STEP 5: MONITOR TRAINING

### Check GPU Usage:
```bash
watch -n 1 nvidia-smi
```

### Monitor Training Log:
```bash
tail -f training.log

# Or with grep for key info:
tail -f training.log | grep -E "Loss|Step|epoch"
```

### Check Progress:
Training will log every 10 steps. Look for:
```
Step 100/9900 - Loss: 1.234
Step 500/9900 - Loss: 0.876
...
```

**Expected Timeline**:
- Steps 0-100: Warmup (2 min)
- Steps 100-9900: Main training (~6.8 hours)
- Final save: (~2 min)
- **Total: ~6.9 hours**

---

## 💾 STEP 6: DOWNLOAD TRAINED ADAPTERS

### After Training Completes:

**On each pod**, the adapter will be saved to:
```
/workspace/output/<entity>_adapter/
├── adapter_model.safetensors  (~50-60MB)
├── adapter_config.json
├── tokenizer_config.json
└── ... (tokenizer files)
```

### Download Methods:

**Option A: Via Jupyter Lab**
1. Open Jupyter Lab (Connect → Jupyter)
2. Navigate to `/workspace/output/<entity>_adapter/`
3. Right-click folder → Download as archive
4. Extract locally

**Option B: Via SCP**
```bash
# From your local machine:
scp -r root@<pod-ip>:/workspace/output/aria_adapter ./aria_adapter
scp -r root@<pod-ip>:/workspace/output/dionysus_adapter ./dionysus_adapter
scp -r root@<pod-ip>:/workspace/output/sage_adapter ./sage_adapter
scp -r root@<pod-ip>:/workspace/output/hydra_adapter ./hydra_adapter
```

**Option C: Via Git**
```bash
# On each pod:
cd /workspace/output
tar -czf <entity>_adapter.tar.gz <entity>_adapter/
# Then download via Jupyter or SCP
```

---

## ✅ STEP 7: VERIFY ADAPTERS

After downloading, verify files locally:

```bash
# Check file sizes
ls -lh aria_adapter/adapter_model.safetensors
ls -lh dionysus_adapter/adapter_model.safetensors
ls -lh sage_adapter/adapter_model.safetensors
ls -lh hydra_adapter/adapter_model.safetensors

# Expected: ~50-60MB each
```

---

## 🏁 STEP 8: SHUTDOWN PODS

**IMPORTANT**: Once training is complete and adapters downloaded:

1. Go to RunPod Console
2. For each pod, click **Stop** or **Terminate**
3. Verify all 4 pods are stopped (no hourly charges!)

**DO NOT** leave pods running - they cost $1.96/hour!

---

## 📋 COMPLETE TIMELINE

```
1:00 PM - 2:00 PM   Setup 4× pods, upload datasets (1 hour)
2:00 PM - 2:30 PM   Install dependencies on all pods (30 min)
2:30 PM - 3:00 PM   Upload scripts, verify setup (30 min)
3:00 PM - 3:15 PM   Start all 4 training jobs simultaneously (15 min)
3:15 PM - 10:00 PM  Training running (6.75 hours)
10:00 PM - 10:30 PM Download adapters (30 min)
10:30 PM - 10:45 PM Verify & backup (15 min)
10:45 PM            Shutdown all pods
```

**Total Cost**: 7 hours × $1.96 (4 pods) = **$13.72**

**Result**: 4× trained LoRA adapters ready for deployment!

---

## 🔧 TROUBLESHOOTING

### Out of Memory Error:
```
RuntimeError: CUDA out of memory
```
**Fix**: Reduce batch size in training script:
```python
"per_device_train_batch_size": 2  # Was 4
"gradient_accumulation_steps": 8  # Was 4
```

### Dataset Not Found:
```
FileNotFoundError: /workspace/datasets/<entity>_final_training.jsonl
```
**Fix**: Verify dataset path and re-upload if needed

### Model Download Slow:
First time downloading Qwen3-30B takes 10-15 minutes. Be patient!

### Training Stops Unexpectedly:
Check `training.log` for errors. Common causes:
- Pod ran out of credits
- Network interruption
- CUDA error (restart pod)

---

## 📞 SUPPORT

**RunPod Issues**: https://www.runpod.io/discord
**Training Questions**: Check `training.log` for detailed error messages

---

## 🎯 SUCCESS CRITERIA

Training is successful when:
- ✅ All 4 scripts complete without errors
- ✅ Each adapter file is ~50-60MB
- ✅ `adapter_config.json` exists for each entity
- ✅ Training loss decreased over time
- ✅ No CUDA errors in logs

---

## 🌊 NEXT STEPS

After training completes:
1. ✅ Download all 4 adapters
2. ✅ Backup to multiple locations
3. Deploy to local Ocean servers (see DEPLOYMENT_GUIDE.md)
4. Test entity intelligence
5. Execute first trade!

**The Ocean awakens!** ⚡
