# Master-Thesis

## Steps for running simulation

1. Git clone the repository using `https://github.com/teodoraalexandra/Master-Thesis.git`
2. Open your IDE and modify `script.sh` accordingly (n, days and aggressivity).

```bash
n=50
days=40
aggressivity=10
persons=$1 # This is the total number of the agents
informed=$2 # This is percentage of informed
```

3. Open a Git Bash and navigate to the root of `Master-Thesis`.
4. Add permissions (only once): `chmod +x script.sh`
5. Run the script: `./script.sh 1000 2`. Note that in this case 1000 and 2 are parameters representing the total number of the agents and the percentage of the informed traders. For the experiments, you should modify these as you need.
6. When the execution is done, the plots will be automatically added to the IMAGES folder.


