FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu20.04

ENV PYENV_SHELL=/bin/bash

RUN set -ex; \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-pip \
    python3-dev && \
    pip install --no-cache-dir --upgrade pip && \
    mkdir -p /app

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["/bin/bash"]