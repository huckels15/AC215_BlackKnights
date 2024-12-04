# Use a lightweight base image with Python
FROM python:3.10-slim

# Set environment variables to minimize interaction during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies for gcloud and apt-transport-https
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    apt-transport-https \
    ca-certificates \
    lsb-release \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Add the new Google Cloud SDK public key and repository
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor > /usr/share/keyrings/cloud.google.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

# Update and install the Google Cloud SDK
RUN apt-get update && apt-get install -y \
    google-cloud-sdk \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /workspace


COPY . /workspace

ENTRYPOINT ["/bin/bash"]
