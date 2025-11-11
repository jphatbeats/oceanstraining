#!/bin/bash
# Download training files from GitHub

cd /workspace
mkdir -p datasets

echo "Downloading setup script..."
wget -O setup_runpod_environment.sh https://raw.githubusercontent.com/jphatbeats/oceanstraining/master/setup_runpod_environment.sh

echo "Downloading training script..."
wget -O train_dionysus_trading_runpod.py https://raw.githubusercontent.com/jphatbeats/oceanstraining/master/train_dionysus_trading_runpod.py

echo "Downloading dataset (20 MB)..."
wget -O datasets/DIONYSUS_trading_brain_ENHANCED.jsonl https://github.com/jphatbeats/oceanstraining/raw/master/data/final_training/DIONYSUS_trading_brain_ENHANCED.jsonl

echo "Done! Verifying..."
ls -lh
wc -l datasets/DIONYSUS_trading_brain_ENHANCED.jsonl
