#!/bin/bash
# Run all 187 blueprints through forge loop-parallel, 3 at a time
set -e
cd /d/styde/_alpedal/styde-forge

total=$(wc -l < blueprint_batches.txt)
start_time=$(date +%s)
completed=0

echo "=== Forge Batch Runner ==="
echo "Total batches: $total"
echo "Blueprints per batch: 3"
echo "Caveman Ultra: ON"
echo "Model: deepseek-v4-flash"
echo "Max iterations: 10"
echo ""

while IFS= read -r batch; do
    [ -z "$batch" ] && continue
    batch_num=$((completed / 3 + 1))
    bp_count=$(echo "$batch" | tr ',' '\n' | wc -l)
    
    echo "--- Batch $batch_num/$total ($(echo $batch | tr ',' ' ')) ---"
    
    if python -u Core/forge.py loop-parallel "$batch" --max 10 --w "$bp_count" 2>&1; then
        completed=$((completed + bp_count))
    else
        echo "  Batch $batch_num FAILED — continuing"
        completed=$((completed + bp_count))
    fi
    
    elapsed=$(( $(date +%s) - start_time ))
    rate=$(echo "scale=1; $completed * 3600 / $elapsed" | bc 2>/dev/null || echo "?")
    echo "  ≈ $completed/187 BPs | ${elapsed}s elapsed | ~${rate} BP/hr"
    echo ""
done < blueprint_batches.txt

elapsed=$(( $(date +%s) - start_time ))
echo "=== ALL DONE ==="
echo "Blueprints: $completed"
echo "Time: $((elapsed / 60))m ${elapsed}s"
