#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
gcloud run deploy puzzlebook \
  --project=personal-ai-264306 \
  --region=europe-west1 \
  --source=. \
  --service-account=puzzlebook-runtime@personal-ai-264306.iam.gserviceaccount.com \
  --execution-environment=gen1 \
  --cpu=0.08 --memory=128Mi --concurrency=1 \
  --min-instances=0 --max-instances=1 \
  --cpu-throttling --no-cpu-boost \
  --allow-unauthenticated --port=8080 --timeout=60 \
  --quiet
