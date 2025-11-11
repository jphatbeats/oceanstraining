# GIT SETUP + RUNPOD WORKFLOW
**Complete guide**: Git setup → Push to GitHub → Pull on RunPod → Train

---

## STEP 1: PUSH TO GITHUB (Do this on your PC)

Your training package is committed to Git locally. Now push it to GitHub so RunPod can pull it.

### Option A: Create New GitHub Repository (Recommended)

**On GitHub.com**:
1. Go to https://github.com/new
2. Repository name: `oceans-training` (or whatever you want)
3. **Private** (recommended - your training data)
4. **Do NOT** initialize with README (we already have files)
5. Click "Create repository"

**On your PC (in Git Bash or PowerShell)**:
```bash
cd N:/OCEANS/oceans_training

# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/oceans-training.git

# Push to GitHub (will prompt for credentials)
git push -u origin master
```

**Note**: If GitHub asks for credentials:
- Username: Your GitHub username
- Password: Use a **Personal Access Token** (not your password!)
  - Get token at: https://github.com/settings/tokens
  - Click "Generate new token (classic)"
  - Select scopes: `repo` (full control)
  - Copy token and use it as password

### Option B: Use Existing Repository

If you already have a GitHub repo:
```bash
cd N:/OCEANS/oceans_training

# Add remote (replace with your actual repo URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push
git push -u origin master
```

---

## STEP 2: PULL ON RUNPOD (Do this on RunPod)

Once pushed to GitHub, you can pull on RunPod.

**On your RunPod pod (in terminal)**:
```bash
# Navigate to workspace
cd /workspace

# Clone your repository
git clone https://github.com/YOUR_USERNAME/oceans-training.git

# (Replace YOUR_USERNAME/oceans-training with your actual repo)

# Enter the directory
cd oceans-training

# Verify files are there
ls -lh setup_runpod_environment.sh
ls -lh train_dionysus_trading_runpod.py
ls -lh data/final_training/DIONYSUS_trading_brain_ENHANCED.jsonl
```

**Note**: If repo is private, you'll need to authenticate:
```bash
# GitHub will prompt for username and token
# Username: Your GitHub username
# Password: Your Personal Access Token
```

---

## STEP 3: RUN SETUP SCRIPT (RunPod)

Now run the setup script to install all packages:

```bash
cd /workspace/oceans-training

# Make script executable
chmod +x setup_runpod_environment.sh

# Run it (takes ~10 minutes)
./setup_runpod_environment.sh
```

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
```

---

## STEP 4: START TRAINING (RunPod)

### For DIONYSUS-TRADING (Start with this one):

```bash
cd /workspace/oceans-training

# Verify dataset
wc -l data/final_training/DIONYSUS_trading_brain_ENHANCED.jsonl
# Should show: 28464

# Start training
nohup python train_dionysus_trading_runpod.py > training.log 2>&1 &

# Monitor progress
tail -f training.log
```

Press `Ctrl+C` to exit tail (training keeps running in background).

---

## STEP 5: MONITOR TRAINING

### Check Progress Anytime:
```bash
# Last 50 lines of log
tail -n 50 /workspace/oceans-training/training.log

# Check GPU usage (should be 90-100%)
nvidia-smi

# Check if still running
ps aux | grep train_dionysus
```

### What You'll See:

**Initial (first 5-10 min)**:
```
======================================================================
TRAINING DIONYSUS_TRADING ON RUNPOD A6000
======================================================================

[1/6] Loading dataset: /workspace/datasets/DIONYSUS_trading_brain_ENHANCED.jsonl
  Loaded 28,464 samples

[2/6] Loading tokenizer: microsoft/Phi-3-mini-4k-instruct

[3/6] Tokenizing dataset...
  Tokenized 28,464 samples

[4/6] Loading base model (4-bit): microsoft/Phi-3-mini-4k-instruct
  This may take 2-3 minutes...
  Base model loaded successfully!

[5/6] Preparing model for k-bit training...
  Trainable params: 4,194,304 (1.54%)

[6/6] Setting up training...

======================================================================
STARTING DIONYSUS_TRADING TRAINING
======================================================================
Steps: 2,500
Estimated time: ~2-3 hours
======================================================================
```

**Mid-Training (after ~1 hour)**:
```
{'loss': 0.85, 'learning_rate': 1.8e-05, 'epoch': 0.4}
{'loss': 0.72, 'learning_rate': 1.6e-05, 'epoch': 0.5}
```

**Completion (after ~3 hours)**:
```
{'loss': 0.18, 'learning_rate': 0.0, 'epoch': 1.0}

======================================================================
DIONYSUS_TRADING TRAINING COMPLETE!
======================================================================

Saving final adapter to /workspace/output/dionysus_trading_adapter...
  Adapter saved: 24.8 MB

======================================================================
SUCCESS!
======================================================================

DONE! Trade execution intelligence UPGRADED!
```

---

## STEP 6: DOWNLOAD ADAPTER

### Verify Adapter Created:
```bash
# Check adapter exists
ls -lh /workspace/oceans-training/output/dionysus_trading_adapter/

# Should show:
# adapter_model.safetensors (~25 MB)
# adapter_config.json
# tokenizer files

# Check size
du -sh /workspace/oceans-training/output/dionysus_trading_adapter/
```

### Download via RunPod Web Interface:

**Note**: Since files are in the Git repo directory, you need to download them through RunPod's web interface or copy them out first.

**Option A: Use RunPod Web File Manager**
1. Navigate to `/workspace/oceans-training/output/dionysus_trading_adapter/`
2. Select all files
3. Download

**Option B: Copy to /workspace for easier download**
```bash
# Copy adapter to /workspace (outside Git repo)
cp -r /workspace/oceans-training/output/dionysus_trading_adapter /workspace/

# Now download from /workspace/dionysus_trading_adapter/
```

**Save locally to**:
`N:\OCEANS\oceans_training\output\dionysus_trading_adapter\`

---

## STEP 7: STOP POD ⚠️ CRITICAL!

**DO NOT FORGET THIS!**

1. Go to RunPod dashboard
2. Find your DIONYSUS-TRADING pod
3. Click "Stop" or "Terminate"
4. Verify status = "Stopped"

If you forget: **$0.49/hour continues charging** ($11.76/day wasted!)

---

## STEP 8: REPEAT FOR OTHER 4 PODS

Once DIONYSUS-TRADING works, repeat for the other 4 pods:

### On each new pod:

```bash
# Pull repo
cd /workspace
git clone https://github.com/YOUR_USERNAME/oceans-training.git
cd oceans-training

# Run setup
chmod +x setup_runpod_environment.sh
./setup_runpod_environment.sh

# Start training (use appropriate script for each pod)
nohup python train_aria_runpod.py > training.log 2>&1 &
# OR
nohup python train_dionysus_runpod.py > training.log 2>&1 &
# OR
nohup python train_sage_runpod.py > training.log 2>&1 &
# OR
nohup python train_hydra_runpod.py > training.log 2>&1 &

# Monitor
tail -f training.log
```

**Run all 4 in parallel** (7 hours each, but all finish at same time!)

---

## ALTERNATIVE: IF GIT LFS ISSUES

If Git LFS doesn't work on RunPod or datasets don't download:

### On RunPod:
```bash
# Clone repo (gets scripts and docs)
cd /workspace
git clone https://github.com/YOUR_USERNAME/oceans-training.git
cd oceans-training

# Run setup script
chmod +x setup_runpod_environment.sh
./setup_runpod_environment.sh

# Create datasets directory
mkdir -p data/final_training

# Download datasets directly from HuggingFace or your storage
# (You'll need to upload datasets separately if Git LFS doesn't work)
```

Then manually upload datasets via RunPod web interface to:
`/workspace/oceans-training/data/final_training/`

---

## QUICK REFERENCE COMMANDS

### On Your PC (Push to GitHub):
```bash
cd N:/OCEANS/oceans_training
git remote add origin https://github.com/YOUR_USERNAME/oceans-training.git
git push -u origin master
```

### On RunPod (Pull and Setup):
```bash
cd /workspace
git clone https://github.com/YOUR_USERNAME/oceans-training.git
cd oceans-training
chmod +x setup_runpod_environment.sh
./setup_runpod_environment.sh
```

### On RunPod (Start Training):
```bash
cd /workspace/oceans-training
wc -l data/final_training/DIONYSUS_trading_brain_ENHANCED.jsonl  # Verify: 28464
nohup python train_dionysus_trading_runpod.py > training.log 2>&1 &
tail -f training.log
```

### On RunPod (After Training):
```bash
# Verify adapter
ls -lh /workspace/oceans-training/output/dionysus_trading_adapter/

# Copy to /workspace for easier download
cp -r /workspace/oceans-training/output/dionysus_trading_adapter /workspace/

# Download via RunPod web interface
# Then STOP POD!
```

---

## TROUBLESHOOTING

### Git LFS datasets don't download on RunPod
**Solution**: Upload datasets manually via RunPod web interface to:
`/workspace/oceans-training/data/final_training/`

### Can't authenticate with GitHub
**Solution**: Use Personal Access Token instead of password
- Get token: https://github.com/settings/tokens
- Use token as password when Git asks

### Setup script fails
**Solution**: Re-run it (safe to run multiple times)
```bash
cd /workspace/oceans-training
./setup_runpod_environment.sh
```

### Training script not found
**Solution**: Make sure you're in the right directory
```bash
cd /workspace/oceans-training
ls -lh train_*.py  # Should see training scripts
```

---

## TIMELINE

**DIONYSUS-TRADING** (First pod - test run):
- Setup: 10 min
- Training: 3 hours
- Download: 5 min
- **Total: ~3.5 hours, $1.75**

**Other 4 pods** (Parallel):
- Setup each: 10 min
- Training: 7 hours (all finish together)
- Download each: 5 min
- **Total: ~7.5 hours wall-clock, $14.70**

**Grand Total**: ~11 hours wall-clock, **~$16.45** for all 5 adapters

---

## NEXT STEPS

1. **Right now**: Push to GitHub (see STEP 1 above)
2. **On RunPod**: Pull repo and run setup script (STEP 2-3)
3. **Start training**: DIONYSUS-TRADING first (STEP 4)
4. **Monitor**: Watch for completion (~3 hours)
5. **Download**: Get adapter (STEP 6)
6. **STOP POD!** (STEP 7)
7. **Repeat**: For other 4 pods (STEP 8)

**The Ocean awakens with trained intelligence!** 🌊⚡
