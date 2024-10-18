# Use the official Python image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy and Run the requirements.txt 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all contents into /app
COPY . .

# Set the credentials which were specified within the shell
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/secrets.json"

CMD ["/bin/bash"]
