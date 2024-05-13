#!/bin/bash

GREEN='\033[0;32m'

param1=$1
param2=$2

echo -e "${GREEN}Building new Docker image..."
docker build -t flash-crash-ntw-anls:latest .
echo -e "${GREEN}Starting docker container and running execution..."
docker run -it --rm flash-crash-ntw-anls:latest ./script.sh "$param1" "$param2"