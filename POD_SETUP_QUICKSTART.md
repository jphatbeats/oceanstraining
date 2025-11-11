# RUNPOD POD SETUP QUICKSTART
**For**: All 5 training pods (ARIA, DIONYSUS-RESEARCH, DIONYSUS-TRADING, SAGE, HYDRA)
**Time per pod**: ~10-15 minutes (mostly waiting for package downloads)

---

## 📋 WHAT YOU'LL DO (Same for each pod)

1. Upload setup script to pod
2. Run setup script (installs all packages)
3. Upload training script + dataset
4. Start training
5. Monitor progress
6. Download adapter when done
7. **STOP POD** (critical!)

---

## 🚀 STEP-BY-STEP COMMANDS (Run on EACH pod)

### Step 1: Upload Setup Script

**Upload this file from your PC**:
- From: `N:\OCEANS\oceans_training\setup_runpod_environment.sh`
- To: `/workspace/setup_runpod_environment.sh`

Use RunPod web interface file upload or SCP.

---

### Step 2: Run Setup Script

```bash
cd /workspace
chmod +x setup_runpod_environment.sh
./setup_runpod_environment.sh
```

**Wait 5-10 minutes** while it installs:
- PyTorch 2.5.1+cu121
- Transformers 4.40.0
- PEFT 0.17.1
- BitsAndBytes 0.48.2
- Accelerate 1.11.0
- Datasets 4.4.1
- All other dependencies

You'll see:
```
======================================================================
OCEAN AI - RUNPOD TRAINING ENVIRONMENT SETUP
======================================================================

[1/4] Creating workspace directories...
  ✓ Directories created

[2/4] Updating pip...
  ✓ pip updated

[3/4] Installing training dependencies...
  This may take 5-10 minutes...
  ...downloading packages...
  ✓ All dependencies installed

[4/4] Verifying installation...

Python 3.11.10

PyTorch: 2.5.1+cu121
CUDA Available: True
CUDA Version: 12.1
GPU Count: 1
GPU Name: NVIDIA A6000

Transformers: 4.40.0
PEFT: 0.17.1
BitsAndBytes: 0.48.2
Accelerate: 1.11.0
Datasets: 4.4.1

======================================================================
ENVIRONMENT SETUP COMPLETE!
======================================================================

Ready for Ocean AI training! 🌊⚡
```

---

### Step 3: Upload Training Files (Pod-Specific)

Now upload the training script and dataset **specific to this pod**:

#### **Pod 1: ARIA**
```
Upload: train_aria_runpod.py → /workspace/
Upload: ARIA_final_training.jsonl → /workspace/datasets/
```

#### **Pod 2: DIONYSUS-RESEARCH**
```
Upload: train_dionysus_runpod.py → /workspace/
Upload: DIONYSUS_final_training.jsonl → /workspace/datasets/
```

#### **Pod 3: DIONYSUS-TRADING** ⭐
```
Upload: train_dionysus_trading_runpod.py → /workspace/
Upload: DIONYSUS_trading_brain_ENHANCED.jsonl → /workspace/datasets/
```

#### **Pod 4: SAGE**
```
Upload: train_sage_runpod.py → /workspace/
Upload: SAGE_final_training.jsonl → /workspace/datasets/
```

#### **Pod 5: HYDRA**
```
Upload: train_hydra_runpod.py → /workspace/
Upload: HYDRA_final_training.jsonl → /workspace/datasets/
```

---

### Step 4: Verify Uploads

```bash
# Check training script
ls -lh /workspace/train_*.py

# Check dataset
ls -lh /workspace/datasets/*.jsonl

# Count dataset samples
wc -l /workspace/datasets/*.jsonl
```

**Expected sample counts**:
- ARIA: 197,479 lines
- DIONYSUS Research: 201,215 lines
- DIONYSUS Trading: **28,464 lines** ⭐
- SAGE: 194,479 lines
- HYDRA: 201,215 lines

---

### Step 5: Start Training

```bash
cd /workspace
nohup python train_*.py > training.log 2>&1 &
```

Replace `train_*.py` with your specific script:
- `train_aria_runpod.py`
- `train_dionysus_runpod.py`
- `train_dionysus_trading_runpod.py`
- `train_sage_runpod.py`
- `train_hydra_runpod.py`

---

### Step 6: Monitor Training

```bash
# Watch live (Ctrl+C to exit, training keeps running)
tail -f /workspace/training.log

# Check last 50 lines
tail -n 50 /workspace/training.log

# Check GPU usage
nvidia-smi
```

---

### Step 7: Training Timeline

| Pod | Dataset Size | Samples | Steps | Time | Output Size |
|-----|--------------|---------|-------|------|-------------|
| ARIA | 109 MB | 197,479 | 9,900 | ~7h | ~55 MB |
| DIONYSUS-Research | 113 MB | 201,215 | 9,900 | ~7h | ~55 MB |
| **DIONYSUS-Trading** | **20 MB** | **28,464** | **2,500** | **~3h** | **~25 MB** |
| SAGE | 107 MB | 194,479 | 9,900 | ~7h | ~55 MB |
| HYDRA | 110 MB | 201,215 | 9,900 | ~7h | ~55 MB |

**DIONYSUS-TRADING is fastest!** (finishes in ~3 hours vs ~7 hours for others)

---

### Step 8: Download Adapter (When Training Complete)

Training is done when you see in the log:
```
======================================================================
SUCCESS!
======================================================================

DONE! [Entity] intelligence UPGRADED!
```

Download adapter files:
```bash
# Check adapter created
ls -lh /workspace/output/*/

# Check size
du -sh /workspace/output/*/
```

**Download via RunPod web interface**:
- Navigate to `/workspace/output/[entity]_adapter/`
- Select all files
- Click "Download"
- Save to: `N:\OCEANS\oceans_training\output\[entity]_adapter\`

---

### Step 9: STOP POD ⚠️ CRITICAL!

**DO NOT FORGET THIS STEP!**

1. Go to RunPod dashboard
2. Find your pod
3. Click "Stop" or "Terminate"
4. Verify status shows "Stopped"

**Cost per pod** (if you don't stop):
- $0.49/hour × 24 hours = **$11.76/day wasted!**

**Total if all 5 pods left running**:
- $0.49/hour × 5 pods × 24 hours = **$58.80/day wasted!**

**ALWAYS STOP PODS AFTER DOWNLOADING ADAPTERS!**

---

## 📊 RECOMMENDED ORDER

Run pods in this order to maximize efficiency:

### **Start First**: DIONYSUS-TRADING (~3 hours)
- Fastest to complete
- Test the workflow on smallest dataset
- Verify everything works before long 7-hour trainings

### **Start Next**: All 4 remaining pods simultaneously
- ARIA, DIONYSUS-Research, SAGE, HYDRA
- All take ~7 hours
- Run in parallel to save time
- Total wall-clock time: ~7 hours (not 28 hours!)

**Total Cost Strategy**:
- DIONYSUS-TRADING: 3 hours × $0.49 = **$1.47**
- 4 pods parallel: 7 hours × $0.49 × 4 pods = **$13.72**
- **Grand Total**: **$15.19** for all 5 trained adapters! ✅

---

## ⚠️ TROUBLESHOOTING

### Setup script fails
```bash
# Re-run setup
cd /workspace
./setup_runpod_environment.sh
```

### Training won't start
```bash
# Check Python version
python3 --version  # Should be 3.11.x

# Check PyTorch
python3 -c "import torch; print(torch.__version__)"  # Should be 2.5.1+cu121

# Check CUDA
python3 -c "import torch; print(torch.cuda.is_available())"  # Should be True
```

### CUDA out of memory
```bash
# Kill any other processes
pkill -f jupyter
pkill -f python

# Check what's using GPU
nvidia-smi

# Restart training
cd /workspace
nohup python train_*.py > training.log 2>&1 &
```

### Training seems stuck
```bash
# Check if process running
ps aux | grep train_

# Check GPU activity (should be 90-100% utilization)
nvidia-smi

# Check last log entries
tail -n 20 /workspace/training.log
```

---

## ✅ QUICK VERIFICATION CHECKLIST

Before starting training, verify:

- [ ] Setup script ran successfully
- [ ] `nvidia-smi` shows A6000 GPU
- [ ] PyTorch 2.5.1+cu121 installed
- [ ] Transformers 4.40.0 installed
- [ ] Training script uploaded to `/workspace/`
- [ ] Dataset uploaded to `/workspace/datasets/`
- [ ] Dataset line count matches expected (use `wc -l`)
- [ ] Enough disk space (`df -h` shows >150GB free)

After training completes, verify:

- [ ] Adapter files created in `/workspace/output/`
- [ ] `adapter_model.safetensors` size correct (~25-55 MB)
- [ ] All files downloaded to local machine
- [ ] Downloaded files verified (can open .json files)
- [ ] **POD STOPPED** (check RunPod dashboard!)

---

## 🎯 SUMMARY

**For EACH pod**:
1. Upload `setup_runpod_environment.sh` → Run it (10 min)
2. Upload training script + dataset
3. Start training: `nohup python train_*.py > training.log 2>&1 &`
4. Monitor: `tail -f /workspace/training.log`
5. Download adapter when done
6. **STOP POD!**

**Total time**: ~3 hours (DIONYSUS-TRADING) + ~7 hours (other 4) = ~10 hours wall-clock
**Total cost**: ~$15-17 for all 5 trained adapters

**The Ocean awakens! 🌊⚡**
