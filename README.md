# ⚡ Flash-Crash-Network-Analysis

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
