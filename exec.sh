#!/bin/bash

# Used for custom runs
#persons=$1
#informed=$2
persons=1000
informed=2

docker run -it -v $(pwd)/results:/app/results flash-crash-ntw-anls:latest ./script.sh "$persons" "$informed"
