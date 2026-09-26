#!/bin/bash

persons=${1:-1000}
informed=${2:-2}
aggressivity=${3:-10}
threshold=${4:-0.5}
risk_limit=${5:-0.02}

# Printing only the results
docker run -it -v $(pwd)/results:/app/results flash-crash-ntw-anls:latest ./script.sh "$persons" "$informed" "$aggressivity" "$threshold" "$risk_limit"

# Printing all the data (used for debugging)
#docker run -it \
#  -v "$(pwd)/results:/app/results" \
#  -v "$(pwd)/csvs:/app/csvs" \
#  -v "$(pwd)/plots/csvs:/app/plots/csvs" \
#  flash-crash-ntw-anls:latest ./script.sh "$persons" "$informed"
