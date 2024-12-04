#!/bin/bash
set -e

echo "Container is running!!!"

mkdir -p /mnt/gcs_data
gcsfuse --implicit-dirs $GCS_BUCKET_NAME /mnt/gcs_data
echo "GCS bucket mounted at /mnt/gcs_data"

mkdir -p /mnt/gcs_data/data
mkdir -p /app/data
mount --bind /mnt/gcs_data/test /app/data
echo "Mounted /mnt/gcs_data/test to /app/data"

uvicorn app:app --port 8000 --host 0.0.0.0