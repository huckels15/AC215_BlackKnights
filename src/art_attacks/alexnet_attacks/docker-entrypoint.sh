#!/bin/bash
set -e

# echo "Container is running!!!"
gsutil -m cp -r gs://alexnet-data-multi/adversarial_testing /app/data

echo "Downloaded data"

uvicorn app:app --host 0.0.0.0 --port 8000