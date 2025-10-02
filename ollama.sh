#! /bin/bash
export OLLAMA_PORT=8090
export OLLAMA_HOST="http://0.0.0.0:${OLLAMA_PORT}"

# Detect available CPU cores
TOTAL_CORES=$(nproc)

# Generate a random number between 1 and 3 (adjustable range)
CPU_CORE_REMOVE=4

# Ensure we don't set cores to 0 or negative
CORES_TO_USE=$((TOTAL_CORES - CPU_CORE_REMOVE))
if [ "$CORES_TO_USE" -lt 1 ]; then
    CORES_TO_USE=1
fi

export OLLAMA_NUM_PARALLEL=$CORES_TO_USE

echo "[CPU INFORMATION] Using $CORES_TO_USE CPU cores out of $TOTAL_CORES"

ollama serve