# Master-Thesis

## Steps for running simulation

1. Git clone the repository using `https://github.com/teodoraalexandra/Master-Thesis.git`
2. Install Docker https://docs.docker.com/engine/install/
3. Run command: `chmod +x exec.sh` This will add permissions
4. Run command: `./exec.sh 1000 2` Note that in this case 1000 and 2 are parameters representing the total number of the agents and the percentage of the informed traders. For the experiments, you should modify these as you need.
5. The simulation will start and the results will be saved in the `results` folder
6. Modify parameters from point (4) and re-run with different parameters to see different results