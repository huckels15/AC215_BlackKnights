#!/bin/bash

# exit immediately if a command exits with a non-zero status
set -e

# Define some environment variables
export IMAGE_NAME="data-download-resnet"
export BASE_DIR=$(pwd)

BUILD="False" 

if [ "$BUILD" == "True" ]; then 
    echo "Building image..."
    docker build -t $IMAGE_NAME -f Dockerfile .

    docker run --rm --name $IMAGE_NAME -ti \
    --mount type=bind,source="$BASE_DIR",target=/app \
    --mount type=bind,source="/mnt/c/Users/Jacob/OneDrive - West Point/Irrelevant BS/Desktop/secrets",target=/app/secrets \
    $IMAGE_NAME
fi

if [ "$BUILD" != "True" ]; then 
    docker run --rm --name $IMAGE_NAME -ti \
    --mount type=bind,source="$BASE_DIR",target=/app \
    --mount type=bind,source="/mnt/c/Users/Jacob/OneDrive - West Point/Irrelevant BS/Desktop/secrets",target=/app/secrets \
    $IMAGE_NAME
fi