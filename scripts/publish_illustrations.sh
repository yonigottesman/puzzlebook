#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
uv run --with pillow python scripts/prepare_illustrations.py "$@"
gcloud storage rsync output/illustrations gs://puzzlebook-images-941271455567/ --checksums-only \
  --content-type=image/webp --cache-control='public,max-age=31536000,immutable'
