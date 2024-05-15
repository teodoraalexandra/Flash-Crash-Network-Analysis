# Master-Thesis

## Steps for running simulation

1. Git clone the repository using `https://github.com/teodoraalexandra/Master-Thesis.git`
2. Install Docker https://docs.docker.com/engine/install/. Make sure that Docker is up and running. 
3. Build Docker image using `docker build -t flash-crash-ntw-anls:latest .`
4. Run command: `chmod +x exec.sh` for the permissions.
5. Run `./exec.sh 1000 2`. Note that in this case 1000 and 2 are parameters representing the total number of the agents and the percentage of the informed traders. For the experiments, you should modify these as you need.
6. The simulation will start and the results will be saved in the `results` folder.

### Notes
* If you modify the code, step (3) should be executed again. 
* If you do not modify the code, and you only want to run the simulation with different parameters, re-run step (5), so you can send the new params to  the `exec.sh` file and see new results.