#!/bin/bash

# Add permissions: chmod +x script.sh
# Run script: ./script.sh

# Set the classpath to include the JAR file and the current directory
classpath="atom-1.14.jar:."

# Remove the csv files autogenerated from previous run
rm -f "PIN_mean.csv"
rm -f "assortativity_mean.csv"
rm -f "bipartivity_mean.csv"

# Compile the Java program with the classpath and the three source files
javac -cp "$classpath" -d . application/src/atomSimulation/Main.java application/src/atomSimulation/InformedAgent.java application/src/atomSimulation/NoiseAgent.java

# Compile all python modules
program_dir="plots/monte-carlo"
module_dirs=("plots/independent" "plots/monte-carlo")
export PYTHONPATH="$program_dir:${module_dirs[0]}:${module_dirs[1]}:${PYTHONPATH}"

for dir in "${module_dirs[@]}"; do
    python3 -m compileall "$dir"
done
python3 -m compileall "$program_dir"

# For loop for our simulations
# Set the number of times to repeat the commands (number of simulations)
n=50

for i in $(seq 1 $n); do
    echo "Start simulation $i..."

    # Run the program and print the output to prices.csv
    java -cp "$classpath" atomSimulation.Main

    cat data.csv | grep "^\(Price\|Day\).*" > plots/prices.csv

    # Run the Python programs for creation
    python3 "$program_dir/PIN_mean_creation.py"
    python3 "$program_dir/assortativity_mean_creation.py"
    python3 "$program_dir/bipartivity_mean_creation.py"
done

# Run the Python program for computation & plot correlations
python3 "$program_dir/correlation_plots.py"