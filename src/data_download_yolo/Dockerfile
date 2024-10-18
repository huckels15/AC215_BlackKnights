# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory (which contains the Python script) into the container
COPY . .

# Ensure the service account key file is available
# You can bind-mount it from the host machine at runtime for security purposes

# Set environment variable for the GCP service account JSON key file path
# (You will bind-mount the key from your host machine to this path at runtime)
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/secrets.json"

# Run the Python script
CMD ["/bin/bash"]
