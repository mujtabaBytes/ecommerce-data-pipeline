#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"
source .venv/bin/activate

echo "========== EXTRACT =========="
python src/extract.py

echo "========== LOAD =========="
python src/load.py

echo "========== TRANSFORM =========="
python src/transform.py

echo "========== PIPELINE COMPLETE =========="
