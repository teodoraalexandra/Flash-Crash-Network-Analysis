# Network Indicators of Information Asymmetry in Fast Trading Markets

📄 This repository contains the code for the paper **"Network Indicators of Information Asymmetry in Fast Trading Markets"**, submitted to the *International Journal of Finance and Economics*.

## 🚀 Steps to Run the Simulation

1. 🧬 **Clone the repository**
   ```bash
   git clone https://github.com/teodoraalexandra/Flash-Crash-Network-Analysis.git
   ```

2. 🐳 **Install Docker**  
   Follow the guide here: [Docker Installation](https://docs.docker.com/engine/install/)  
   Make sure Docker is up and running before moving on!

3. 🏗️ **Build the Docker image**
   ```bash
   docker build -t flash-crash-ntw-anls:latest .
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
docker build -t flash-crash-ntw-anls:latest .
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
