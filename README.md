# Master-Thesis

## Steps for running simulation

1. Git clone the repository using `https://github.com/teodoraalexandra/Master-Thesis.git`
2. Install the Docker https://docs.docker.com/engine/install/
3. Run command: `chmod +x exec.sh`
4. Run command: `./exec.sh`
5. The simulation will start and the results will be saved in the `images` folder
6. You can modify the code and the parameters at `Dockerfile: ex: CMD [ "./script.sh", "1000", "10"]`
7. After each modification, run again `./exec.sh`'