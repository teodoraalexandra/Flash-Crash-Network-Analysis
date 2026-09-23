#!/bin/bash

persons=${1:-1000}
informed=${2:-2}
aggressivity=${3:-10}
threshold=${4:-0.5}
risk_limit=${5:-0.02}

docker run -it -v $(pwd)/results:/app/results flash-crash-ntw-anls:latest ./script.sh "$persons" "$informed" "$aggressivity" "$threshold" "$risk_limit"
