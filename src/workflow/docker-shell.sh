#!/bin/bash

# set -e

export IMAGE_NAME="ac215-black-knights-workflow"
export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../../../secrets/
export GCP_PROJECT="secret-cipher-399620"
export GCS_BUCKET_NAME="resnet-models-ac215"
export GCS_SERVICE_ACCOUNT="ml-workflow@secret-cipher-399620.iam.gserviceaccount.com"
export GCP_REGION="us-east1"
export GCS_PACKAGE_URI="gs://resnet-trainer"

# Build the image based on the Dockerfile
#docker build -t $IMAGE_NAME -f Dockerfile .
docker build -t $IMAGE_NAME --platform=linux/amd64 -f Dockerfile .


# Run Container
docker run --rm --name $IMAGE_NAME -ti \
-v /var/run/docker.sock:/var/run/docker.sock \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/secrets \
-e GOOGLE_APPLICATION_CREDENTIALS=/secrets/ml-workflow.json \
-e GCP_PROJECT=$GCP_PROJECT \
-e GCS_BUCKET_NAME=$GCS_BUCKET_NAME \
-e GCS_SERVICE_ACCOUNT=$GCS_SERVICE_ACCOUNT \
-e GCP_REGION=$GCP_REGION \
-e GCS_PACKAGE_URI=$GCS_PACKAGE_URI \
-e WANDB_KEY=$WANDB_KEY \
$IMAGE_NAME

