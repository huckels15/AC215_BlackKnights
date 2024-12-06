#!/bin/bash

set -e

BUILD="False" 

export IMAGE_NAME="endpoint_testing"
export BASE_DIR=$(pwd)
export GCP_PROJECT="secret-cipher-399620"
export GCP_ZONE="us-east1"

if [ "$BUILD" == "True" ]; then 
    echo "Building image..."
    docker build -t $IMAGE_NAME -f Dockerfile .

    docker run --rm --name $IMAGE_NAME -ti \
        --privileged \
        --cap-add SYS_ADMIN \
        --device /dev/fuse \
        --mount type=bind,source="$BASE_DIR",target=/workspace \
        -e GCP_PROJECT=$GCP_PROJECT \
        -e GCP_ZONE=$GCP_ZONE \
        -p 8000:8000 \
        $IMAGE_NAME
    fi

if [ "$BUILD" != "True" ]; then 
    echo "Using prebuilt image..."
    docker run --rm --name $IMAGE_NAME -ti \
        --privileged \
        --cap-add SYS_ADMIN \
        --device /dev/fuse \
        --mount type=bind,source="$BASE_DIR",target=/workspace \
        -e GCP_PROJECT=$GCP_PROJECT \
        -e GCP_ZONE=$GCP_ZONE \
        -p 8000:8000 \
        $IMAGE_NAME
fi