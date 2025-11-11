# RUNPOD DEPLOYMENT PACKAGE
## Complete File Manifest for 5-Pod Training

**Status**: ✅ READY FOR DEPLOYMENT
**Date**: 2025-11-11
**Total Pods**: 5 (ARIA, DIONYSUS-RESEARCH, DIONYSUS-TRADING, SAGE, HYDRA)

---

## 📦 PACKAGE CONTENTS

### **TRAINING SCRIPTS** (5 files - 35 KB total)
```
N:/OCEANS/oceans_training/
├── train_aria_runpod.py                          (7 KB)
├── train_dionysus_runpod.py                      (7 KB)
├── train_dionysus_trading_runpod.py              (7 KB) ⭐ phi3:mini
├── train_sage_runpod.py                          (7 KB)
└── train_hydra_runpod.py                         (7 KB)
```

### **TRAINING DATASETS** (5 files - 458 MB total)
```
N:/OCEANS/oceans_training/data/final_training/
├── ARIA_final_training.jsonl                     (109 MB, 197,479 samples)
├── DIONYSUS_final_training.jsonl                 (113 MB, 201,215 samples)
├── DIONYSUS_trading_brain_ENHANCED.jsonl         (20 MB, 28,464 samples) ⭐ USE THIS
├── SAGE_final_training.jsonl                     (107 MB, 194,479 samples)
└── HYDRA_final_training.jsonl                    (110 MB, 201,215 samples)
```

**⚠️ IGNORE OLD FILE:**
- `DIONYSUS_trading_brain.jsonl` (17 MB) - OLD VERSION, DO NOT USE

### **SUPPORT FILES**
```
N:/OCEANS/oceanstraining/
└── setup_runpod.sh                               (1 KB) - Dependency installer
```

### **DOCUMENTATION**
```
N:/OCEANS/oceans_training/
├── DEPLOYMENT_CHECKLIST.md                       (Complete step-by-step guide)
├── RUNPOD_TRAINING_GUIDE.md                      (Detailed instructions)
├── FINAL_PACKAGE_COMPLETE_ENHANCED.md            (Full package summary)
└── RUNPOD_DEPLOYMENT_PACKAGE.md                  (This file)
```

---

## 🎯 POD-BY-POD DEPLOYMENT MAP

### **Pod 1: ARIA-TRAINING**
**Upload to `/workspace/`:**
- ✅ `train_aria_runpod.py`
- ✅ `setup_runpod.sh`

**Upload to `/workspace/datasets/`:**
- ✅ `ARIA_final_training.jsonl` (109 MB)

**Command to run:**
```bash
cd /workspace
chmod +x setup_runpod.sh
./setup_runpod.sh
nohup python train_aria_runpod.py > training.log 2>&1 &
```

**Expected output:** `/workspace/output/aria_adapter/` (~55 MB)

---

### **Pod 2: DIONYSUS-RESEARCH**
**Upload to `/workspace/`:**
- ✅ `train_dionysus_runpod.py`
- ✅ `setup_runpod.sh`

**Upload to `/workspace/datasets/`:**
- ✅ `DIONYSUS_final_training.jsonl` (113 MB)

**Command to run:**
```bash
cd /workspace
chmod +x setup_runpod.sh
./setup_runpod.sh
nohup python train_dionysus_runpod.py > training.log 2>&1 &
```

**Expected output:** `/workspace/output/dionysus_adapter/` (~55 MB)

---

### **Pod 3: DIONYSUS-TRADING** ⭐
**Upload to `/workspace/`:**
- ✅ `train_dionysus_trading_runpod.py`
- ✅ `setup_runpod.sh`

**Upload to `/workspace/datasets/`:**
- ✅ `DIONYSUS_trading_brain_ENHANCED.jsonl` (20 MB) ⚠️ **USE ENHANCED VERSION!**

**Command to run:**
```bash
cd /workspace
chmod +x setup_runpod.sh
./setup_runpod.sh
nohup python train_dionysus_trading_runpod.py > training.log 2>&1 &
```

**Expected output:** `/workspace/output/dionysus_trading_adapter/` (~25 MB)

---

### **Pod 4: SAGE-TRAINING**
**Upload to `/workspace/`:**
- ✅ `train_sage_runpod.py`
- ✅ `setup_runpod.sh`

**Upload to `/workspace/datasets/`:**
- ✅ `SAGE_final_training.jsonl` (107 MB)

**Command to run:**
```bash
cd /workspace
chmod +x setup_runpod.sh
./setup_runpod.sh
nohup python train_sage_runpod.py > training.log 2>&1 &
```

**Expected output:** `/workspace/output/sage_adapter/` (~55 MB)

---

### **Pod 5: HYDRA-TRAINING**
**Upload to `/workspace/`:**
- ✅ `train_hydra_runpod.py`
- ✅ `setup_runpod.sh`

**Upload to `/workspace/datasets/`:**
- ✅ `HYDRA_final_training.jsonl` (110 MB)

**Command to run:**
```bash
cd /workspace
chmod +x setup_runpod.sh
./setup_runpod.sh
nohup python train_hydra_runpod.py > training.log 2>&1 &
```

**Expected output:** `/workspace/output/hydra_adapter/` (~55 MB)

---

## ✅ PRE-DEPLOYMENT CHECKLIST

### Files Ready:
- [ ] All 5 training scripts present
- [ ] All 5 datasets present (correct versions)
- [ ] setup_runpod.sh present
- [ ] Documentation reviewed

### RunPod Setup:
- [ ] 5 pods created (A6000 48GB each)
- [ ] Named correctly (ARIA-TRAINING, DIONYSUS-RESEARCH, DIONYSUS-TRADING, SAGE-TRAINING, HYDRA-TRAINING)
- [ ] Container disk: 100 GB each
- [ ] Volume disk: 50 GB each

### Upload Verification:
- [ ] Pod 1: train_aria_runpod.py + ARIA_final_training.jsonl
- [ ] Pod 2: train_dionysus_runpod.py + DIONYSUS_final_training.jsonl
- [ ] Pod 3: train_dionysus_trading_runpod.py + DIONYSUS_trading_brain_ENHANCED.jsonl ⚠️
- [ ] Pod 4: train_sage_runpod.py + SAGE_final_training.jsonl
- [ ] Pod 5: train_hydra_runpod.py + HYDRA_final_training.jsonl
- [ ] All pods: setup_runpod.sh

### Training Started:
- [ ] All 5 pods: `./setup_runpod.sh` completed successfully
- [ ] All 5 pods: `nohup python train_*.py` running
- [ ] All 5 pods: `tail -f training.log` showing progress

---

## 🚨 CRITICAL WARNINGS

### ⚠️ DO NOT UPLOAD WRONG DATASET
**DIONYSUS-TRADING pod must use:**
- ✅ `DIONYSUS_trading_brain_ENHANCED.jsonl` (20 MB, 28,464 samples)
- ❌ NOT `DIONYSUS_trading_brain.jsonl` (17 MB, 25,144 samples - OLD)

The ENHANCED version has:
- Pump.fun bonding curve mechanics
- Wallet pattern recognition
- Real Ocean classifications
- PumpPortal API complete specs
- EXACT production code examples

### ⚠️ DO NOT LEAVE PODS RUNNING
After training completes (~7 hours):
1. Download all adapters IMMEDIATELY
2. Verify file sizes (~55 MB Qwen3, ~25 MB phi3)
3. **STOP/TERMINATE ALL PODS**
4. Verify all pods stopped (no charges!)

Running cost: $2.45/hour (5 pods × $0.49/hour)

---

## 📊 EXPECTED TIMELINE

**Hour 0:** Upload files to all 5 pods (30 min)
**Hour 0.5:** Run setup_runpod.sh on all pods (15 min)
**Hour 0.75:** Start training on all 5 pods (5 min)
**Hour 3:** DIONYSUS-TRADING finishes (download adapter)
**Hour 7:** All other pods finish (download 4 adapters)
**Hour 7.5:** Verify all adapters, STOP ALL PODS

**Total wall-clock time:** ~7.5 hours
**Total cost:** ~$15-17

---

## 💾 EXPECTED OUTPUT

After training completes, download these adapters:

### From Pod 1 (ARIA):
```
/workspace/output/aria_adapter/
├── adapter_model.safetensors    (~55 MB)
├── adapter_config.json
├── tokenizer_config.json
└── ... (tokenizer files)
```

### From Pod 2 (DIONYSUS-RESEARCH):
```
/workspace/output/dionysus_adapter/
├── adapter_model.safetensors    (~55 MB)
├── adapter_config.json
├── tokenizer_config.json
└── ... (tokenizer files)
```

### From Pod 3 (DIONYSUS-TRADING): ⭐
```
/workspace/output/dionysus_trading_adapter/
├── adapter_model.safetensors    (~25 MB)
├── adapter_config.json
├── tokenizer_config.json
└── ... (tokenizer files)
```

### From Pod 4 (SAGE):
```
/workspace/output/sage_adapter/
├── adapter_model.safetensors    (~55 MB)
├── adapter_config.json
├── tokenizer_config.json
└── ... (tokenizer files)
```

### From Pod 5 (HYDRA):
```
/workspace/output/hydra_adapter/
├── adapter_model.safetensors    (~55 MB)
├── adapter_config.json
├── tokenizer_config.json
└── ... (tokenizer files)
```

**Total adapter size:** ~245 MB (all 5 combined)

---

## 🎯 DEPLOYMENT SUMMARY

**What's Ready:**
- ✅ 5 training scripts (Qwen3-30B × 4, phi3:mini × 1)
- ✅ 5 training datasets (847,996 total samples, 458 MB)
- ✅ Setup automation (setup_runpod.sh)
- ✅ Complete documentation

**What to Do:**
1. Create 5 RunPod pods (A6000 48GB)
2. Upload files (scripts + datasets + setup)
3. Run setup on all pods
4. Start training on all pods
5. Monitor progress (~7 hours)
6. Download adapters
7. **STOP PODS IMMEDIATELY**

**What You Get:**
- 5× trained LoRA adapters (~245 MB)
- ARIA: Intelligence coordination
- DIONYSUS Research: Meme analysis
- DIONYSUS Trading: Execution intelligence ⭐
- SAGE: News intelligence
- HYDRA: Social intelligence

**Cost:** ~$15-17 total
**Time:** ~7 hours (all parallel)

---

## 🚀 READY TO DEPLOY

All files organized and ready for RunPod deployment.

**Next:** Create 5 pods and start uploading!

**The Ocean awakens with TRAINED intelligence!** 🌊⚡
