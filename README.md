# Master-Thesis

## Steps for running simulation

1. Using predefined Atom Script

```bash
// Syntax: <nbAgents> <nbOrderbooks> <nbTurns> <nbDays>
java -cp atom-1.14.jar fr.cristal.smac.atom.Generate 10 1 1000 1 > plots/data.csv
java -cp atom-1.14.jar fr.cristal.smac.atom.Generate 100 1 1000 1 | grep "^Price" > plots/prices.csv
```

Plot using plotNetwork.py, plotPriceEvolution.py or plotQuantityEvolution.py

2. Using your own Script

* Run Main from atomSimulation.
* cat data.csv | grep "^Price" > plots/prices.csv
* Plot the same :)


