#!/bin/bash

set -e

export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../../../secrets/
export GCS_BUCKET_NAME="traffic-sign-dataset"
export GCP_PROJECT="ac215-black-knights"
export GCP_ZONE="us-east4"
export GOOGLE_APPLICATION_CREDENTIALS="/secrets/data-service-account.json"


BUILD="False" 

if [ "$BUILD" == "True" ]; then 
    echo "Building image"
    docker build -t data-version-cli-yolo -f Dockerfile .

    echo "Running container"
    docker run --rm --name data-version-cli-yolo -ti \
    --privileged \
    --cap-add SYS_ADMIN \
    --device /dev/fuse \
    -v "$BASE_DIR":/app \
    -v "$SECRETS_DIR":/secrets \
    -v ~/.gitconfig:/etc/gitconfig \
    -v "$(pwd)/../../":/git_repo \
    -e GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS \
    -e GCP_PROJECT=$GCP_PROJECT \
    -e GCP_ZONE=$GCP_ZONE \
    -e GCS_BUCKET_NAME=$GCS_BUCKET_NAME data-version-cli-yolo
fi

if [ "$BUILD" == "False" ]; then 
    echo "Running container"
    docker run --rm --name data-version-cli-yolo -ti \
    --privileged \
    --cap-add SYS_ADMIN \
    --device /dev/fuse \
    -v "$BASE_DIR":/app \
    -v "$SECRETS_DIR":/secrets \
    -v ~/.gitconfig:/etc/gitconfig \
    -v "$(pwd)/../../":/git_repo \
    -e GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS \
    -e GCP_PROJECT=$GCP_PROJECT \
    -e GCP_ZONE=$GCP_ZONE \
    -e GCS_BUCKET_NAME=$GCS_BUCKET_NAME data-version-cli-yolo
fi