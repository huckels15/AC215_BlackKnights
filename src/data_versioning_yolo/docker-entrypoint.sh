#!/bin/bash

echo "Container is running!!!"


gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
mkdir -p /mnt/gcs_bucket
gcsfuse --key-file=$GOOGLE_APPLICATION_CREDENTIALS $GCS_BUCKET_NAME /mnt/gcs_data
echo 'GCS bucket mounted at /mnt/gcs_data'
mkdir -p /app/yolo_dataset
mount --bind /mnt/gcs_data/dvc_store/data /git_repo/src/data_versioning_yolo/yolo_dataset

pipenv shell