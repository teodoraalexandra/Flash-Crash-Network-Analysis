#!/bin/bash

# Used for custom runs
#persons=$1
#informed=$2
persons=1000
informed=2

# Printing only the results
docker run -it -v $(pwd)/results:/app/results flash-crash-ntw-anls:latest ./script.sh "$persons" "$informed"

# Printing all the data (used for debugging)
#docker run -it \
#  -v "$(pwd)/results:/app/results" \
#  -v "$(pwd)/csvs:/app/csvs" \
#  -v "$(pwd)/plots/csvs:/app/plots/csvs" \
#  flash-crash-ntw-anls:latest ./script.sh "$persons" "$informed"
