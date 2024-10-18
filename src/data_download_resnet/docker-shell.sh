#!/bin/bash

# exit immediately if a command exits with a non-zero status
set -e

# Define some environment variables
export IMAGE_NAME="data-download-resnet"
export BASE_DIR=$(pwd)

echo "Building image..."
docker build -t $IMAGE_NAME -f Dockerfile .

# Run the container
docker run --rm --name $IMAGE_NAME -ti \
--mount type=bind,source="$BASE_DIR",target=/app \
--mount type=bind,source="/home/elijahdabkowski/AY25-1/classes/AC215/project/secrets/",target=/app/secrets \
$IMAGE_NAME
