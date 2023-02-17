#!/bin/bash

# Add permissions: chmod +x script.sh
# Run script: ./script.sh

# Set the classpath to include the JAR file and the current directory
classpath="atom-1.14.jar:."

# Compile the Java program with the classpath and the three source files
javac -cp "$classpath" -d . application/src/atomSimulation/Main.java application/src/atomSimulation/InformedAgent.java application/src/atomSimulation/NoiseAgent.java

# Run the program and print the output to prices.csv
java -cp "$classpath" atomSimulation.Main

cat data.csv | grep "^\(Price\|Day\).*" > plots/prices.csv

# Compile all python modules
program_dir="plots/monte-carlo"
module_dirs=("plots/independent" "plots/monte-carlo")
export PYTHONPATH="$program_dir:${module_dirs[0]}:${module_dirs[1]}:${PYTHONPATH}"

for dir in "${module_dirs[@]}"; do
    python3 -m compileall "$dir"
done
python3 -m compileall "$program_dir"

# Run the Python program for creation
python3 "$program_dir/PIN_mean_creation.py"

# Run the Python program for computation
python3 "$program_dir/PIN_mean_computation.py"