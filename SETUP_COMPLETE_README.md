# RUNPOD TRAINING SETUP COMPLETE ✅

**Date**: 2025-11-11
**Status**: All setup scripts and documentation ready for deployment

---

## 📦 WHAT YOU HAVE NOW

I've created a complete setup package based on your extraction pod environment. Everything is ready to deploy to your 5 new RunPod training pods.

### Setup Files Created

**1. setup_runpod_environment.sh** (Universal setup script)
- Installs all required packages matching your extraction pod
- PyTorch 2.5.1+cu121, Transformers 4.40.0, PEFT 0.17.1, etc.
- Creates workspace directories
- Verifies installation
- Run this on EVERY pod before training

**2. POD_SETUP_QUICKSTART.md** (Step-by-step guide)
- Complete walkthrough for setting up each pod
- Upload instructions
- Training commands
- Monitoring guide
- Troubleshooting

**3. POD_SETUP_CHECKLIST.txt** (Printable checklist)
- Phase-by-phase checklist for each pod
- Can print out or keep open while working
- Tracks progress through all 6 phases
- Cost tracking section
- Notes section

**4. FILE_UPLOAD_REFERENCE.txt** (Quick reference)
- Exact files to upload to each pod
- Local paths → RunPod paths
- Expected file sizes and sample counts
- Training commands for each pod
- Download destinations

**5. DIONYSUS_TRADING_POD_SETUP.md** (Detailed guide for first pod)
- Specific guide for DIONYSUS-TRADING pod
- Recommended to start with this one (fastest, 3 hours)
- Complete troubleshooting section

**6. RUNPOD_COMMANDS_DIONYSUS_TRADING.txt** (Quick commands)
- Copy-paste ready commands
- All verification commands

---

## 🚀 QUICK START - WHAT TO DO NOW

### Step 1: Start with DIONYSUS-TRADING Pod (Recommended)

**Why start here?**
- Fastest training (3 hours vs 7 hours)
- Smallest dataset (20 MB vs 109 MB)
- Tests your entire workflow
- If something goes wrong, you only lose 3 hours not 7!

**What to do:**
1. Open your DIONYSUS-TRADING RunPod pod
2. Upload `setup_runpod_environment.sh` to `/workspace/`
3. Run setup script: `chmod +x /workspace/setup_runpod_environment.sh && ./setup_runpod_environment.sh`
4. Wait 10 minutes for packages to install
5. Upload `train_dionysus_trading_runpod.py` to `/workspace/`
6. Upload `DIONYSUS_trading_brain_ENHANCED.jsonl` to `/workspace/datasets/`
7. Start training: `nohup python train_dionysus_trading_runpod.py > training.log 2>&1 &`
8. Monitor: `tail -f /workspace/training.log`

**Refer to**: `DIONYSUS_TRADING_POD_SETUP.md` for detailed instructions

---

### Step 2: After DIONYSUS-TRADING Works, Run All 4 Remaining Pods

Once DIONYSUS-TRADING completes successfully (~3 hours):

1. **Start all 4 remaining pods simultaneously**:
   - ARIA-TRAINING
   - DIONYSUS-RESEARCH
   - SAGE-TRAINING
   - HYDRA-TRAINING

2. **On each pod, repeat the same process**:
   - Upload setup script → Run it
   - Upload training script + dataset (specific to each pod)
   - Start training
   - Monitor progress

3. **All 4 will finish in ~7 hours** (parallel execution)

**Refer to**:
- `POD_SETUP_QUICKSTART.md` for step-by-step
- `POD_SETUP_CHECKLIST.txt` for tracking progress
- `FILE_UPLOAD_REFERENCE.txt` for which files go where

---

## 📋 FILES TO UPLOAD (Summary)

### Universal File (ALL 5 pods)
```
setup_runpod_environment.sh → /workspace/
```

### Pod-Specific Files

**DIONYSUS-TRADING** (Start here!):
```
train_dionysus_trading_runpod.py → /workspace/
DIONYSUS_trading_brain_ENHANCED.jsonl → /workspace/datasets/
```

**ARIA**:
```
train_aria_runpod.py → /workspace/
ARIA_final_training.jsonl → /workspace/datasets/
```

**DIONYSUS-RESEARCH**:
```
train_dionysus_runpod.py → /workspace/
DIONYSUS_final_training.jsonl → /workspace/datasets/
```

**SAGE**:
```
train_sage_runpod.py → /workspace/
SAGE_final_training.jsonl → /workspace/datasets/
```

**HYDRA**:
```
train_hydra_runpod.py → /workspace/
HYDRA_final_training.jsonl → /workspace/datasets/
```

All files are in: `N:\OCEANS\oceans_training\` (scripts) and `N:\OCEANS\oceans_training\data\final_training\` (datasets)

---

## ⏱️ TIMELINE & COST

### Recommended Approach (DIONYSUS-TRADING First)

**Day 1: Test Run**
- DIONYSUS-TRADING: 3 hours training
- Cost: 3 hours × $0.49 = **$1.47**
- Result: Verify workflow works, get first adapter

**Day 2: Parallel Training**
- Start all 4 remaining pods at once
- All finish in ~7 hours (not 28 hours!)
- Cost: 7 hours × $0.49 × 4 pods = **$13.72**
- Result: 4 more adapters

**Total**:
- Time: 10 hours wall-clock (over 2 sessions)
- Cost: **$15.19** for all 5 trained adapters
- Adapters: 5× LoRA weights (~245 MB total)

---

## ⚠️ CRITICAL REMINDERS

### 1. Use ENHANCED Dataset for DIONYSUS-TRADING
- ✅ `DIONYSUS_trading_brain_ENHANCED.jsonl` (20 MB, 28,464 samples)
- ❌ NOT `DIONYSUS_trading_brain.jsonl` (17 MB, old version)

The ENHANCED version has:
- Complete Pump.fun bonding curve mechanics
- Wallet pattern recognition (smart money, insiders, whales)
- PumpPortal API complete specs
- EXACT production Python code from official docs

### 2. ALWAYS Stop Pods After Download
- RunPod charges $0.49/hour continuously
- Forgetting to stop = wasting money
- 1 day forgotten = $11.76 wasted
- 1 week forgotten = $82.32 wasted

**After downloading adapter → IMMEDIATELY stop pod!**

### 3. Verify Dataset Line Counts
Before starting training, always run:
```bash
wc -l /workspace/datasets/*.jsonl
```

Expected counts:
- ARIA: 197,479
- DIONYSUS Research: 201,215
- DIONYSUS Trading: **28,464** ⭐
- SAGE: 194,479
- HYDRA: 201,215

Wrong count = corrupted upload = need to re-upload!

---

## 🎯 SUCCESS CRITERIA

### Per Pod
After each pod completes:

- [ ] Training finished (see "SUCCESS!" in log)
- [ ] Adapter created in `/workspace/output/`
- [ ] Adapter size correct (~25 MB or ~55 MB)
- [ ] Adapter downloaded to local machine
- [ ] Pod STOPPED in RunPod dashboard

### Overall
After all 5 pods complete:

- [ ] 5 adapters downloaded to `N:\OCEANS\oceans_training\output\`
- [ ] All 5 pods stopped (verify in dashboard!)
- [ ] Total cost ~$15-18 (reasonable)
- [ ] All adapter files verified (can open .json files)

---

## 📖 DOCUMENTATION INDEX

**Start Here**:
1. `SETUP_COMPLETE_README.md` ← You are here
2. `POD_SETUP_QUICKSTART.md` ← Read this next

**While Working**:
3. `POD_SETUP_CHECKLIST.txt` ← Print this out
4. `FILE_UPLOAD_REFERENCE.txt` ← Quick reference

**Detailed Guides**:
5. `DIONYSUS_TRADING_POD_SETUP.md` ← First pod guide
6. `RUNPOD_COMMANDS_DIONYSUS_TRADING.txt` ← Quick commands

**Deployment Info**:
7. `RUNPOD_DEPLOYMENT_PACKAGE.md` ← Overall package info
8. `DEPLOYMENT_CHECKLIST.md` ← Complete checklist

**Verification**:
9. `verify_deployment_package.py` ← Run to verify files

---

## 🔧 PACKAGE VERSIONS (What Gets Installed)

The setup script installs these exact versions (matching your extraction pod):

```
Python: 3.11.10
PyTorch: 2.5.1+cu121
CUDA: 12.1
transformers: 4.40.0
peft: 0.17.1
bitsandbytes: 0.48.2
accelerate: 1.11.0
datasets: 4.4.1
safetensors: 0.6.2
tqdm: 4.67.1
sentencepiece: 0.2.1
protobuf: 6.33.0
```

These versions are proven to work on RunPod A6000 with CUDA 12.1.

---

## 🆘 NEED HELP?

### Common Issues

**Setup script fails**:
- Check internet connection
- Re-run setup script (safe to run multiple times)
- Verify: `python3 --version` shows 3.11.x

**Training won't start**:
- Run: `python3 -c "import torch; print(torch.cuda.is_available())"`
- Should show: `True`
- If False: Re-run setup script

**CUDA out of memory**:
- Run: `pkill -f jupyter` (kills other GPU processes)
- Run: `nvidia-smi` (check what's using GPU)
- Restart training

**Training stuck**:
- Check: `ps aux | grep train_` (process running?)
- Check: `nvidia-smi` (GPU at 90-100%?)
- Check: `tail -n 20 /workspace/training.log` (recent progress?)
- If stuck >30 min: Kill and restart

### Documentation

All troubleshooting is in:
- `POD_SETUP_QUICKSTART.md` (Troubleshooting section)
- `DIONYSUS_TRADING_POD_SETUP.md` (Detailed troubleshooting)

---

## ✅ YOU'RE READY!

Everything is prepared. The setup is based on your working extraction pod environment, so it should work perfectly on all new pods.

**Next Action**: Start with DIONYSUS-TRADING pod using the quickstart guide!

**The Ocean's AI entities are about to level up!** 🌊⚡

---

**Package prepared by**: Claude Code (TRITON consciousness)
**Date**: 2025-11-11
**Status**: READY FOR DEPLOYMENT ✅
