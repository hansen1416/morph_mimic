#!/bin/bash
# SPDX-FileCopyrightText: Copyright (c) 2026 Longzhen Han
# SPDX-License-Identifier: Apache-2.0
# Frame-0 grounding offsets for the 16 HUMOS motion chunks (humos_131072_0000 .. 0015).
# Usage, from the repository root:
#   DATA_DIR=/path/to/humos_proto bash tools/run_frame0_offsets.sh
# Optional: ASSET_ROOT (default: protomotions/data/assets/mjcf/smpl_mor).
set -e

DATA_DIR="${DATA_DIR:?Set DATA_DIR to the directory holding humos_131072_NNNN.pt}"
ASSET_ROOT="${ASSET_ROOT:-protomotions/data/assets/mjcf/smpl_mor}"
mkdir -p "${DATA_DIR}/offset"

for i in $(seq -f "%04g" 0 15); do
    echo "=== Processing chunk $i ==="
    python tools/compute_humos_frame0_offsets.py \
        --motion-file "${DATA_DIR}/humos_131072_${i}.pt" \
        --asset-root "${ASSET_ROOT}" \
        --out-motion-file "${DATA_DIR}/offset/humos_131072_${i}_offset.pt" \
        --limit -1 \
        --overwrite
done

echo "=== All 16 chunks done ==="
