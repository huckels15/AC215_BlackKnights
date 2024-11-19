FROM nvidia/cuda:11.3.1-cudnn8-runtime-ubuntu20.04

ENV PYENV_SHELL=/bin/bash
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

RUN set -ex; \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    libavcodec-extra \
    vim \
    git \
    libgl1-mesa-glx \
    build-essential \
    python3-pip \
    python3-dev && \
    pip install --no-cache-dir --upgrade pip && \
    mkdir -p /app

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

ENTRYPOINT ["/bin/bash"]