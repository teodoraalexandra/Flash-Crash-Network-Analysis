# Network Indicators of Information Asymmetry in Fast Trading Markets

📄 This repository contains the code for the paper **"Network Indicators of Information Asymmetry in Fast Trading Markets"**, submitted to the *International Journal of Finance and Economics*.

## 🚀 Steps to Run the Simulation

1. 🧬 **Clone the repository**
   ```bash
   git clone https://github.com/teodoraalexandra/information-asymmetry-networks.git
   ```

2. 🐳 **Install Docker**  
   Follow the guide here: [Docker Installation](https://docs.docker.com/engine/install/)  
   Make sure Docker is up and running before moving on!

3. 🏗️ **Build the Docker image**
   ```bash
   docker build -t information-asymmetry-networks:latest .
   ```

4. 🛡️ **Set permissions (Linux only)**
   ```bash
   chmod +x exec.sh
   ```  
   ✅ Windows users can skip this step.

5. ▶️ **Start the simulation**
   - 📟 **Linux**
     ```bash
     ./exec.sh
     ```  
   - 🪟 **Windows**
     ```powershell
     ./exec_windows.ps1
     ```

   ⚙️ **Custom parameters (optional)**  
   `exec.sh` accepts five positional arguments. If you omit them, the defaults (the baseline configuration) are used:

   ```bash
   ./exec.sh <persons> <informed%> <aggressivity γ> <threshold τ> <risk limit>
   #  e.g.   ./exec.sh 1000 2 10 0.5 0.02   (this is the baseline)
   ```

   | Argument | Meaning | Baseline value |
   |---|---|---|
   | `persons` | Total number of agents in the market | `1000` |
   | `informed%` | Share of informed traders (% of population) | `2` |
   | `aggressivity γ` | Aggressiveness of informed traders | `10` |
   | `threshold τ` | Activation threshold of informed traders | `0.5` |
   | `risk limit` | Risk limit per agent | `0.02` |

   ---

   ### 🔁 Reproducing **all** the `results_*` folders

   The repository contains several pre-computed result folders (`results_baseline`, `results_g5`, `results_alt_log`, …). Each one is simply the `results` folder of a single run with a specific configuration, copied and renamed. Follow the three phases below **in order** to regenerate all of them.

   > ⚠️ Every run **overwrites** the `results` folder, so always `cp -r results results_<name>` right after a run finishes. And remember: whenever you edit `script.sh` or the Java code, you must **rebuild the Docker image** (step 3) before running again.

   **Phase 1 — Baseline (with the bucket-size sensitivity heatmap)**

   1. Open `script.sh` and **enable** the heatmap step by removing the `#` in front of `pythonBucketSensitivity` (near the bottom of the file):
      ```bash
      # HEATMAP Generation
      pythonBucketSensitivity
      ```
   2. Rebuild the image (step 3), then run:
      ```bash
      ./exec.sh 1000 2 10 0.5 0.02 && cp -r results results_baseline
      ```

   **Phase 2 — Parameter sensitivity sweep (heatmap disabled)**

   1. Open `script.sh` again and **disable** the heatmap step by putting the `#` back:
      ```bash
      # HEATMAP Generation
      #pythonBucketSensitivity
      ```
   2. Rebuild the image (step 3), then run all eight variations. Each one changes **exactly one** parameter relative to the baseline:
      ```bash
      ./exec.sh 1000 2 5  0.5 0.02 && cp -r results results_g5    && \
      ./exec.sh 1000 2 20 0.5 0.02 && cp -r results results_g20   && \
      ./exec.sh 1000 1 10 0.5 0.02 && cp -r results results_inf1  && \
      ./exec.sh 1000 8 10 0.5 0.02 && cp -r results results_inf8  && \
      ./exec.sh 1000 2 10 0.3 0.02 && cp -r results results_t03   && \
      ./exec.sh 1000 2 10 0.7 0.02 && cp -r results results_t07   && \
      ./exec.sh 1000 2 10 0.5 0.01 && cp -r results results_risk1 && \
      ./exec.sh 1000 2 10 0.5 0.05 && cp -r results results_risk5
      ```

      | Folder | What changed vs. baseline |
      |---|---|
      | `results_g5` | aggressiveness γ = 5 (lower) |
      | `results_g20` | aggressiveness γ = 20 (higher) |
      | `results_inf1` | 1% informed traders (fewer) |
      | `results_inf8` | 8% informed traders (more) |
      | `results_t03` | activation threshold τ = 0.3 (lower) |
      | `results_t07` | activation threshold τ = 0.7 (higher) |
      | `results_risk1` | risk limit = 1% (tighter) |
      | `results_risk5` | risk limit = 5% (looser) |

   **Phase 3 — Alternative information diffusion (logarithmic)**

   1. Open `src/InformedAgent.java` and switch the informed traders to the **logarithmic** diffusion model: in `calculateInformationLevel`, comment out the power-law line and uncomment the logarithmic one:
      ```java
      public double calculateInformationLevel(double time) {
          //return diffusionCoefficient * Math.pow(time, anomalousExponent);

          // Alternative — logarithmic diffusion
          return diffusionCoefficient * Math.log(time + 1);
      }
      ```
   2. Rebuild the image (step 3), then run the baseline parameters again:
      ```bash
      ./exec.sh 1000 2 10 0.5 0.02 && cp -r results results_alt_log
      ```
   3. 🔙 Afterwards, revert `src/InformedAgent.java` to the original (power-law) line so future runs use the default model.

   **Final step — Collect the sensitivity summary**

   Once all the `results_*` folders exist, aggregate the VPIN–metric correlations across all configurations into `sensitivity_results.txt`:
   ```bash
   python3 collect_sensitivity.py
   ```

6. ⏳ **Be patient**  
   The simulation includes multiple components and may take a while.  
   You can check `script.sh` to see how many simulations are scheduled.

   🔍 The script includes:
   - 📊 **pythonGraphMetricsPart**: Calculates graph metrics (e.g., assortativity, components)
   - 💰 **pythonAgentCashPart**: Analyzes agent cash distribution
   - 🖼️ **pythonVisualGraphs**: Generates visual graphs

   💡 Tip: To run only one part, comment out the others in `script.sh`.

7. 📁 **Results**  
   All output will be saved in the `results` folder.

---

### 📝 Notes

- 🔄 **If you modify the code**: Repeat step (3) to rebuild the Docker image.

---

## 🔬 Reproducing the Paper Results

The `results_*` folders are produced in three stages. The arguments to `exec.sh` are, in order: `persons`, `informed (%)`, `aggressivity`, `threshold`, `risk_limit`.

⚠️ After **every** change to `script.sh` or the Java code, rebuild the Docker image before running:
```bash
docker build -t information-asymmetry-networks:latest .
```

1. 🎯 **Baseline** — enable `pythonBucketSensitivity` in `script.sh` (uncomment the call), rebuild, then run:
   ```bash
   ./exec.sh 1000 2 10 0.5 0.02 && cp -r results results_baseline
   ```

2. 📈 **Sensitivity runs** — remove (comment out) `pythonBucketSensitivity` in `script.sh`, rebuild, then run:
   ```bash
   ./exec.sh 1000 2 5  0.5 0.02 && cp -r results results_g5 && \
   ./exec.sh 1000 2 20 0.5 0.02 && cp -r results results_g20 && \
   ./exec.sh 1000 1 10 0.5 0.02 && cp -r results results_inf1 && \
   ./exec.sh 1000 8 10 0.5 0.02 && cp -r results results_inf8 && \
   ./exec.sh 1000 2 10 0.3 0.02 && cp -r results results_t03 && \
   ./exec.sh 1000 2 10 0.7 0.02 && cp -r results results_t07 && \
   ./exec.sh 1000 2 10 0.5 0.01 && cp -r results results_risk1 && \
   ./exec.sh 1000 2 10 0.5 0.05 && cp -r results results_risk5
   ```

3. 🪵 **Alternative logarithmic diffusion** — in `src/InformedAgent.java`, switch `calculateInformationLevel` to the alternative logarithmic diffusion (comment the power law, uncomment the `Math.log` line), rebuild, then run:
   ```bash
   ./exec.sh 1000 2 10 0.5 0.02 && cp -r results results_alt_log
   ```

Finally, aggregate all runs into the sensitivity comparison table:
```bash
python3 collect_sensitivity.py
```
