#!/bin/bash

# Used for custom runs
#   ./exec.sh 1000 2 10 0.5 0.02     # explicit baseline
#   ./exec.sh 1000 2 5  0.5 0.02     # vary aggressiveness
#   ./exec.sh 1000 1 10 0.5 0.02     # vary population share
#   ./exec.sh 1000 2 10 0.3 0.02     # vary activation threshold
#   ./exec.sh 1000 2 10 0.5 0.01     # vary risk limit
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
