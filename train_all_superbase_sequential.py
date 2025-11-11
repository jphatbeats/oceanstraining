"""
Sequential Super-Base Training Orchestrator
Trains all 3 super-bases sequentially: ARIA → SAGE → HYDRA
Monitors progress and handles errors automatically
"""

import subprocess
import time
import sys
from pathlib import Path

# Training scripts in execution order
TRAINING_SEQUENCE = [
    {
        'name': 'ARIA',
        'script': 'train_aria_superbase.py',
        'log': 'aria_superbase_FINAL.log',
        'status_file': 'outputs_aria_superbase/final_model/config.json'
    },
    {
        'name': 'SAGE',
        'script': 'train_sage_superbase.py',
        'log': 'sage_superbase_FINAL.log',
        'status_file': 'outputs_sage_superbase/final_model/config.json'
    },
    {
        'name': 'HYDRA',
        'script': 'train_hydra_superbase.py',
        'log': 'hydra_superbase_FINAL.log',
        'status_file': 'outputs_hydra_superbase/final_model/config.json'
    }
]

def train_entity(config):
    """Train a single entity and return success status"""
    print("=" * 70, flush=True)
    print(f"STARTING {config['name']} SUPER-BASE TRAINING", flush=True)
    print("=" * 70, flush=True)
    print(f"Script: {config['script']}", flush=True)
    print(f"Log: {config['log']}", flush=True)
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
    print("=" * 70 + "\n", flush=True)

    start_time = time.time()

    # Run training script
    cmd = f"python -u {config['script']}"

    try:
        with open(config['log'], 'w') as log_file:
            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            # Stream output to both console and log file
            for line in process.stdout:
                print(line, end='', flush=True)
                log_file.write(line)
                log_file.flush()

            process.wait()

            if process.returncode == 0:
                duration = time.time() - start_time
                hours = int(duration // 3600)
                minutes = int((duration % 3600) // 60)

                print("\n" + "=" * 70, flush=True)
                print(f"{config['name']} TRAINING COMPLETE!", flush=True)
                print(f"Duration: {hours}h {minutes}m", flush=True)
                print(f"Final model should be at: {config['status_file']}", flush=True)
                print("=" * 70 + "\n", flush=True)

                return True
            else:
                print("\n" + "=" * 70, flush=True)
                print(f"ERROR: {config['name']} training failed with code {process.returncode}", flush=True)
                print("=" * 70 + "\n", flush=True)
                return False

    except Exception as e:
        print(f"\nEXCEPTION during {config['name']} training: {e}", flush=True)
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main orchestration loop"""
    print("\n" + "=" * 70, flush=True)
    print("SUPER-BASE TRAINING ORCHESTRATOR", flush=True)
    print("=" * 70, flush=True)
    print(f"Training sequence: {' → '.join([c['name'] for c in TRAINING_SEQUENCE])}", flush=True)
    print(f"Total entities: {len(TRAINING_SEQUENCE)}", flush=True)
    print(f"Estimated total time: 4-6 hours", flush=True)
    print(f"Start time: {time.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
    print("=" * 70 + "\n", flush=True)

    overall_start = time.time()
    results = []

    for i, config in enumerate(TRAINING_SEQUENCE, 1):
        print(f"\n[{i}/{len(TRAINING_SEQUENCE)}] Processing {config['name']}...\n", flush=True)
        success = train_entity(config)
        results.append((config['name'], success))

        if not success:
            print(f"\nWARNING: {config['name']} training failed. Stopping sequence.", flush=True)
            break

    # Final summary
    overall_duration = time.time() - overall_start
    hours = int(overall_duration // 3600)
    minutes = int((overall_duration % 3600) // 60)

    print("\n" + "=" * 70, flush=True)
    print("SUPER-BASE TRAINING SUMMARY", flush=True)
    print("=" * 70, flush=True)

    for name, success in results:
        status = "SUCCESS" if success else "FAILED"
        print(f"{status}: {name}", flush=True)

    successful = sum(1 for _, s in results if s)
    print(f"\nTotal: {successful}/{len(TRAINING_SEQUENCE)} entities trained successfully", flush=True)
    print(f"Total time: {hours}h {minutes}m", flush=True)
    print(f"End time: {time.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
    print("=" * 70, flush=True)

    # Exit code: 0 if all successful, 1 otherwise
    return 0 if successful == len(TRAINING_SEQUENCE) else 1

if __name__ == "__main__":
    sys.exit(main())
