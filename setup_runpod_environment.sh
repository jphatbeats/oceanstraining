#!/bin/bash
##############################################################################
# RUNPOD TRAINING ENVIRONMENT SETUP
##############################################################################
# Sets up Python environment for Ocean AI training on RunPod A6000 48GB
# Based on working extraction pod environment
#
# Usage:
#   chmod +x setup_runpod_environment.sh
#   ./setup_runpod_environment.sh
#
# Run this on EACH new RunPod pod before uploading training files
##############################################################################

set -e  # Exit on any error

echo "======================================================================"
echo "OCEAN AI - RUNPOD TRAINING ENVIRONMENT SETUP"
echo "======================================================================"
echo ""

# Create workspace directories
echo "[1/4] Creating workspace directories..."
mkdir -p /workspace/datasets
mkdir -p /workspace/output
mkdir -p /workspace/.cache
echo "  ✓ Directories created"
echo ""

# Update pip
echo "[2/4] Updating pip..."
pip install --upgrade pip
echo "  ✓ pip updated"
echo ""

# Install core training dependencies (matching extraction pod versions)
echo "[3/4] Installing training dependencies..."
echo "  This may take 5-10 minutes..."
echo ""

pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu121

pip install \
    transformers==4.40.0 \
    peft==0.17.1 \
    bitsandbytes==0.48.2 \
    accelerate==1.11.0 \
    datasets==4.4.1 \
    safetensors==0.6.2 \
    tqdm==4.67.1 \
    sentencepiece==0.2.1 \
    protobuf==6.33.0

echo ""
echo "  ✓ All dependencies installed"
echo ""

# Verify installation
echo "[4/4] Verifying installation..."
echo ""

python3 --version
echo ""

python3 -c "import torch; print(f'PyTorch: {torch.__version__}')"
python3 -c "import torch; print(f'CUDA Available: {torch.cuda.is_available()}')"
python3 -c "import torch; print(f'CUDA Version: {torch.version.cuda}')"
python3 -c "import torch; print(f'GPU Count: {torch.cuda.device_count()}')"
if [ $(python3 -c "import torch; print(torch.cuda.device_count())") -gt 0 ]; then
    python3 -c "import torch; print(f'GPU Name: {torch.cuda.get_device_name(0)}')"
fi
echo ""

python3 -c "import transformers; print(f'Transformers: {transformers.__version__}')"
python3 -c "import peft; print(f'PEFT: {peft.__version__}')"
python3 -c "import bitsandbytes; print(f'BitsAndBytes: {bitsandbytes.__version__}')"
python3 -c "import accelerate; print(f'Accelerate: {accelerate.__version__}')"
python3 -c "import datasets; print(f'Datasets: {datasets.__version__}')"
echo ""

echo "======================================================================"
echo "ENVIRONMENT SETUP COMPLETE!"
echo "======================================================================"
echo ""
echo "Installed packages:"
echo "  ✓ PyTorch 2.5.1+cu121 (CUDA 12.1)"
echo "  ✓ Transformers 4.40.0"
echo "  ✓ PEFT 0.17.1 (LoRA training)"
echo "  ✓ BitsAndBytes 0.48.2 (4-bit quantization)"
echo "  ✓ Accelerate 1.11.0 (distributed training)"
echo "  ✓ Datasets 4.4.1 (data loading)"
echo ""
echo "Workspace directories:"
echo "  /workspace/datasets/  - Upload training datasets here"
echo "  /workspace/output/    - Trained adapters saved here"
echo "  /workspace/.cache/    - HuggingFace model cache"
echo ""
echo "Next steps:"
echo "  1. Upload training script to /workspace/"
echo "  2. Upload dataset to /workspace/datasets/"
echo "  3. Run training: nohup python train_*.py > training.log 2>&1 &"
echo ""
echo "Ready for Ocean AI training! 🌊⚡"
echo ""
