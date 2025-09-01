# Use Python image built for ARM architecture
FROM python:3.9-slim-buster
# Install OpenJDK 11 and bash
RUN apt-get update && apt-get install -y openjdk-11-jdk bash

# Set working directory
WORKDIR /app

# Copy the script and required files
COPY script.sh .
COPY . .
COPY requirements.txt .

# Define a volume for the results
VOLUME /app/results
VOLUME /app/csvs
VOLUME /app/plots/csvs

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt --verbose

# Set execute permissions for the script
RUN chmod +x script.sh
