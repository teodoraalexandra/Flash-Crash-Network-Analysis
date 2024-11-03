#!/bin/bash

start=$(date +%s.%N)
# Add permissions: chmod +x script.sh
# Run script: ./script.sh

mkdir -p csvs
mkdir -p plots/csvs

# Remove the csv files autogenerated from previous run & pictures
rm -f csvs/*
rm -f plots/csvs/*

# Compile the Java program
javac -cp atom-1.14.jar src/Main.java src/NoiseAgent.java src/InformedAgent.java src/MarketMaker.java src/InformationPair.java

ROOT_FOLDER=$(dirname "$(realpath "$0")")
export PYTHONPATH=$ROOT_FOLDER

# For loop for our simulations
# Set the number of times to repeat the commands (number of simulations)
n=75
days=40
aggressivity=10
persons=$1 # This is the total number of the agents
informed=$2 # This is percentage of informed

javaPart() {
  local i=$1

  # Run the program and print the output to prices.csv
  # Require 4 arguments: NUMBER_OF_PERSONS, PERCENTAGE_OF_INFORMED, AGGRESSIVITY, DAYS_OF_SIMULATION
  java -classpath "src:atom-1.14.jar" Main "$persons" "$informed" "$aggressivity" "$days" "$i"
  cat "csvs/data$i.csv" | grep "^Price" > "plots/csvs/prices$i$persons$informed.csv"
  cat "csvs/data$i.csv" | grep "^\(Agent\|Day\).*" > "plots/csvs/agents$i.csv"
  sed -i '/noname/d' "plots/csvs/prices$i$persons$informed.csv"
}

callJava() {
  echo "Start Java Simulation..."
  for i in $(seq 1 $n); do
      javaPart "$i" &
  done
  wait
}

pythonGraphMetricsPart() {
  total_rows=$(cat plots/csvs/prices1"$persons""$informed".csv | wc -l)
  big_granularity=$((total_rows / 50))
  small_granularity=$((total_rows / 1000))

  echo "Start Python Computation (Network metrics part)..."

  # Run the Python program for creation
  python "$ROOT_FOLDER"/plots/monte-carlo/graph_metrics.py $n "$persons" "$informed" $big_granularity $small_granularity $days
  echo -e "Metrics graphs was generated. \n"
}

pythonAgentCashPart() {
  echo "Start Python Computation (Agents' Cash Part)..."

  # Run the Python program for plotting agents' cash
  python "$ROOT_FOLDER"/plots/monte-carlo/agent_cash.py $n "$persons" "$informed" $days
  echo -e "Agents' cash evolution graph was generated. \n"
}

pythonLaplacianMetricsPart() {
  echo "Start Python Computation (Laplacian Metrics Part)..."

  # Run the Python program for computing laplacian metrics
  python "$ROOT_FOLDER"/plots/monte-carlo/laplacian_metrics.py $n "$persons" "$informed"
  echo -e "Laplacian graph was generated. \n"
}

pythonGephiGraphs() {
  total_rows=$(cat plots/csvs/prices1"$persons""$informed".csv | wc -l)
  big_granularity=$((total_rows * 2662 / 10000))
  small_granularity=$((total_rows * 2662 / 100000))

  echo "Start Python Computation (Graph Gephi)..."

  # Run the Python program for computing graph complex metrics
  python plots/monte-carlo/gephi_graphs.py $n "$persons" "$informed" $big_granularity $small_granularity
  echo -e "Graph gephi was generated. \n"
}

echo "Running bash script with $persons agents and $informed percentage"

callJava

pythonGraphMetricsPart
pythonAgentCashPart
#pythonLaplacianMetricsPart

# Use this only for generating gml files
#pythonGephiGraphs

end=$(date +%s.%N)
runtime=$(python -c "print(${end} - ${start})")

echo "Runtime was $runtime seconds."