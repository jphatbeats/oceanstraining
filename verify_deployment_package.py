"""
VERIFY RUNPOD DEPLOYMENT PACKAGE
=================================
Checks that all required files are present and correct before deployment
"""

from pathlib import Path
import sys

print("=" * 70)
print("RUNPOD DEPLOYMENT PACKAGE VERIFICATION")
print("=" * 70)

# Define expected files
TRAINING_SCRIPTS = [
    "train_aria_runpod.py",
    "train_dionysus_runpod.py",
    "train_dionysus_trading_runpod.py",
    "train_sage_runpod.py",
    "train_hydra_runpod.py"
]

DATASETS = {
    "ARIA_final_training.jsonl": (109, 197479),  # (size_mb, samples)
    "DIONYSUS_final_training.jsonl": (113, 201215),
    "DIONYSUS_trading_brain_ENHANCED.jsonl": (20, 28464),
    "SAGE_final_training.jsonl": (107, 194479),
    "HYDRA_final_training.jsonl": (110, 201215)
}

SUPPORT_FILES = [
    "../oceanstraining/setup_runpod.sh"
]

# Paths
BASE_DIR = Path("N:/OCEANS/oceans_training")
DATASET_DIR = BASE_DIR / "data" / "final_training"

errors = []
warnings = []

print("\n[1/3] Checking training scripts...")
for script in TRAINING_SCRIPTS:
    script_path = BASE_DIR / script
    if script_path.exists():
        size_kb = script_path.stat().st_size / 1024
        print(f"  [OK] {script} ({size_kb:.1f} KB)")
    else:
        errors.append(f"MISSING: {script}")
        print(f"  [X] {script} - NOT FOUND")

print("\n[2/3] Checking training datasets...")
for dataset, (expected_mb, expected_samples) in DATASETS.items():
    dataset_path = DATASET_DIR / dataset
    if dataset_path.exists():
        size_mb = dataset_path.stat().st_size / (1024 * 1024)

        # Count samples
        sample_count = 0
        try:
            with open(dataset_path, 'r', encoding='utf-8') as f:
                for line in f:
                    sample_count += 1
        except:
            sample_count = 0

        # Check if size is close (within 10%)
        size_ok = abs(size_mb - expected_mb) < (expected_mb * 0.1)
        samples_ok = sample_count == expected_samples

        if size_ok and samples_ok:
            print(f"  [OK] {dataset}")
            print(f"       Size: {size_mb:.1f} MB (expected ~{expected_mb} MB)")
            print(f"       Samples: {sample_count:,} (expected {expected_samples:,})")
        else:
            if not size_ok:
                warnings.append(f"{dataset}: Size mismatch ({size_mb:.1f} MB vs {expected_mb} MB)")
                print(f"  [!] {dataset} - Size mismatch")
            if not samples_ok:
                warnings.append(f"{dataset}: Sample count mismatch ({sample_count:,} vs {expected_samples:,})")
                print(f"  [!] {dataset} - Sample count mismatch")
    else:
        errors.append(f"MISSING: {dataset}")
        print(f"  [X] {dataset} - NOT FOUND")

# Check for old dataset
old_dataset = DATASET_DIR / "DIONYSUS_trading_brain.jsonl"
if old_dataset.exists():
    warnings.append("OLD dataset still present: DIONYSUS_trading_brain.jsonl (should use ENHANCED version)")
    print(f"\n  [!] WARNING: Old DIONYSUS_trading_brain.jsonl found")
    print(f"      Make sure to use DIONYSUS_trading_brain_ENHANCED.jsonl instead!")

print("\n[3/3] Checking support files...")
for support_file in SUPPORT_FILES:
    support_path = BASE_DIR / support_file
    if support_path.exists():
        print(f"  [OK] {support_file}")
    else:
        errors.append(f"MISSING: {support_file}")
        print(f"  [X] {support_file} - NOT FOUND")

# Summary
print("\n" + "=" * 70)
print("VERIFICATION SUMMARY")
print("=" * 70)

if not errors and not warnings:
    print("\n[SUCCESS] All files present and correct!")
    print("\nDeployment package ready for RunPod:")
    print("  - 5 training scripts")
    print("  - 5 training datasets (847,996 samples, 458 MB)")
    print("  - Support files")
    print("\nNext: Create 5 RunPod pods and upload files")
    sys.exit(0)
elif not errors and warnings:
    print(f"\n[WARNINGS] Package ready but with {len(warnings)} warnings:")
    for warning in warnings:
        print(f"  - {warning}")
    print("\nPackage can be deployed but review warnings above.")
    sys.exit(0)
else:
    print(f"\n[ERRORS] Package NOT ready! {len(errors)} errors found:")
    for error in errors:
        print(f"  - {error}")
    if warnings:
        print(f"\nAlso {len(warnings)} warnings:")
        for warning in warnings:
            print(f"  - {warning}")
    print("\nFix errors before deploying!")
    sys.exit(1)
