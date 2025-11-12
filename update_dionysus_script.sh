#!/bin/bash
# Update DIONYSUS training script with tokenizer fix

cd /workspace

echo "Downloading fixed training script..."
wget -O train_dionysus_trading_runpod_FIXED.py https://raw.githubusercontent.com/jphatbeats/oceanstraining/master/train_dionysus_trading_runpod_FIXED.py

echo "Done! Fixed script downloaded."
echo "Now run: pkill -f train_dionysus"
echo "Then run: nohup python train_dionysus_trading_runpod_FIXED.py > training.log 2>&1 &"
